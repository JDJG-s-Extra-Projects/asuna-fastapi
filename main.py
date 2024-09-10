import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

app = FastAPI()

current_directory = pathlib.Path(__file__).absolute().parent
images_directory = pathlib.Path(str(current_directory) + "/images")

# possible better spot for it may exist.
# possibly write usage.json to a database instead for speed reasons.


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


if __name__ == "__main__":

    uvicorn.run("main:app", port=42069, log_level="debug")
