import json
import pathlib
import random
from contextlib import asynccontextmanager
from typing import Dict

import asqlite
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asqlite.create_pool("usage.db") as app.pool:
        yield
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(lifespan=lifespan)


async def get_conn():
    async with app.pool.acquire() as conn:
        yield conn


def get_particular_data(table):
    async def wrapper(conn: asqlite.Connection = Depends(get_conn)):
        async with conn.cursor() as cursor:
            result = await cursor.execute(f"SELECT * FROM {table}")
            return [x[0] for x in await result.fetchall()]

    return wrapper


# Now using the dependency to get data from the 'objection' table
data: list[str] = Depends(get_particular_data("objection"))


current_directory = pathlib.Path(__file__).absolute().parent
images_directory = current_directory / "images"


# Load usage data from JSON file (you can replace this with database loading)
with open("example_usage.json", "r") as f:
    initial_usage_data: Dict = json.load(f)


@app.get("/")
async def welcome():
    return "Welcome to the Asuna fastapi version."


@app.get("/usage")
@cache(expire=60)  # Cache usage data for 60 seconds
async def get_usage():
    # Retrieve usage data from cache (or initial data if not in cache)
    usage_data = FastAPICache.get("usage_data")
    if usage_data is None:
        usage_data = initial_usage_data
        FastAPICache.set("usage_data", usage_data, expire=60)

    return JSONResponse(usage_data)



@app.get("/api/random/{image_type}")
async def get_random_image(image_type: str):
    image_type = image_type.lower()
    image_path = images_directory / image_type

    if not image_path.exists() or not image_path.is_dir():
        raise HTTPException(status_code=404, detail="Picture category not found or there are no images in this category")

    images = [f for f in image_path.iterdir() if f.is_file()]
    if not images:
        raise HTTPException(status_code=404, detail="No images found in this category")

    random_image = random.choice(images)
    return FileResponse(random_image)


@app.get("/api/{image_type}")
async def get_random_image_info(image_type: str, request: Request):
    image_type = image_type.lower()
    image_path = images_directory / image_type

    if not image_path.exists() or not image_path.is_dir():
        raise HTTPException(status_code=404, detail="Picture category not found or there are no images in this category")

    images = [f for f in image_path.iterdir() if f.is_file()]
    if not images:
        raise HTTPException(status_code=404, detail="No images found in this category")

    random_image = random.choice(images)
    return JSONResponse(
        {"fileName": random_image.name, "url": request.url_for("serve_image", image_type=image_type, image_file=random_image.name)}
    )


@app.get("/api")
async def get_endpoints(request: Request):
    total_images = 0
    response = {}

    for endpoint in images_directory.iterdir():
        if endpoint.is_dir():
            category_images = [f for f in endpoint.iterdir() if f.is_file()]
            response[endpoint.name] = {
                "url": str(request.url_for("get_random_image_info", image_type=endpoint.name)),  # Convert URL to string
                "imageCount": len(category_images),
            }
            total_images += len(category_images)

    return JSONResponse({"allEndpoints": list(response.keys()), "endpointInfo": response, "totalImages": total_images})

@app.get("/images/{image_type}/image/{image_file}", name="serve_image")
async def serve_image(image_type: str, image_file: str):
    image_type = image_type.lower()
    image_path = images_directory / image_type / image_file

    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(image_path)


@app.get("/images")
async def missing_image_type():
    raise HTTPException(status_code=400, detail="The file category is required")



@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all():
    html_404_page = pathlib.Path(__file__).parent / "pages/404.html"
    
    if not html_404_page.exists():
        return HTMLResponse(content="<h1>404 - Not Found</h1><p>The requested resource could not be found.</p>", status_code=404)
    
    html_content = html_404_page.read_text()
    return HTMLResponse(content=html_content, status_code=404)


if __name__ == "__main__":
    uvicorn.run("main:app", port=42069, log_level="debug")