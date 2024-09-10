import json
import pathlib
import typing
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asqlite.create_pool("usage.db") as app.pool:
        yield


app = FastAPI()
# do lifespan=lifespan when ready.


def get_particular_data(table):
    async def wrapper(conn=Depends(get_conn)):
        async with conn.cursor() as cursor:
            result = await cursor.execute(f"SELECT * FROM {table}")
            return [x[0] for x in await result.fetchall()]

    return wrapper


# modify this table value
# data: typehint = Depends(get_particular_data("objection")


current_directory = pathlib.Path(__file__).absolute().parent
images_directory = pathlib.Path(str(current_directory) + "/images")

# possible better spot for it may exist.
# possibly write usage.json to a database instead for speed reasons.


with open("example_usage.json", "r") as f:
    usage_data = json.load(f)


@app.get("/")
async def welcome():
    return "Welcome to the Asuna fastapi version."
    # placeholder


@app.get("/usage")
async def get_usage():

    # load example_usage.json for rn
    return JSONResponse(usage_data)
    # use some lifetime object example jdjgapi to in this case grab the usage data


@app.get("/api/{image_type}")
async def get_random_image(image_type: str):
    image_type = image_type.lower()
    images = []

    # in our version I am going to make a check to make sure the image_type exists first.

    image_path = pathlib.Path(str(images_directory) + "/{image_type}")

    if not image_path.exists():
        return JSONResponse({"error": "Picture category not found or there are no images in this category"})

    # if it exists make sure the image_type is within the images folder to prevent fileserver injection
    # list images after this.
    # add to usage like f"{image_type}" or just image_type.
    # ie example neko
    # ./images/{type}/{random_image}"

    # an online accquitance decided to make this ai version for some reason
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L28


@app.get("/api/{image_type}")
async def get_random_image_info(image_type: str):
    image_type = image_type.lower()
    images = []

    image_path = pathlib.Path(str(images_directory) + "/{image_type}")

    if not image_path.exists():
        return JSONResponse({"error": "Picture category not found or there are no images in this category"})

    # if it exists make sure the image_type is within the images folder to prevent fileserver injection
    # list images after this.
    # add to usage like f"{image_type-api}" or just image_type.
    # i.e. example neko-api
    # {"fileName": random_image, "url": f"{url}/images/{type}/image/{random_image}"}

    # an online accquitance decided to make this ai version for some reason
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L60


@app.get("/api")
async def get_endpoints():

    total_images = 0
    response = {}

    endpoints = [path for path in path.iterdir() if path.is_dir()]

    for path in endpoints:
        category_images = [path for path in endpoint.iterdir() if path.is_file()]

        response[path.name] = {"url": f"{base_url}api/{endpoint.name}/", "imageCount": len(category_images)}
        total_images += len(category_images)

    return JSONResponse({"allEndpoints": endpoints, "endpointInfo": response, "totalImages": total_images})


@app.get("/images/{image_type}/image/{image_file}")
async def serve_image(image_type: typing.Optional[str] = None, image_file: typing.Optional[str] = None):

    if image_type is None:
        return JSONResponse({"error": "The file category is required"})

    if file is None:
        return JSONResponse({"error": "The file name is required"})

    image_type = image_type.lower()

    # check if file exists with pathlib
    # if file does not exist:
    # {"error": "File not found"}

    # usage normal of {image_type} like neko

    # an online aqquitance sent me this file made by ai:
    # https://mystb.in/a56e9985c52d7bb3e1?lines=F1-L94


@app.get("/images")
async def missing_image_type():
    return JSONResponse({"error": "The file category is required"})


# 404 response return html
# "<div style='text-align:center'><h3><a href='./'>Go Home</a><br/>4owo4 page not found</div>"
# for any url that does not exist on here.
# this will be displayed with return HTMLResponse


# 404 response for undefined routes
@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all(full_path: str):
    return HTMLResponse(
        content="<div style='text-align:center'><h3><a href='/'>Go Home</a><br/>4owo4 page not found</div>",
        status_code=404,
    )


if __name__ == "__main__":

    uvicorn.run("main:app", port=42069, log_level="debug")
    print(f"Running Web Server on: {base_url}")
