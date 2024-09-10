import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

current_directory = pathlib.Path(__file__).absolute().parent
images_directory = pathlib.Path(str(current_directory) + "/images")
# possible better spot for it may exist.

# possibly write usage.json to a database instead for speed reasons.

# '/api/:type': 'random image from {type/folder}' asuna.ga/api/images/hug/image/hug01.gif
#'/api/: 'list of folders/types' {url: "asuna.ga/api/images/hug", imageCount: 20} //loop through each folder and count contents
# '/images/:type?/image/:file?': 'specific image from specific fodler' imageFile
# /api/usage -> gives usage api stored in a json file possibly this time we might use sqlite ?
# images -> error page because it doesn't ask for specific image.

# /api/random/:type -> gives random file response based on the type you give it.
# /images/:type?/image/:file -> file handling.

# fastapi responses
# return FileResponse(some_file_path) can be used for the image returning on the proper route.
# HTMLResponse -> used for general response.
# JSONResponse -> used for most routes.



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


# api/:type
# convert types to lowercase
# images list
# tries to read the images and type of the folder if it fails with in an invalid error it then uses {error: "Picture category not found or there are no images in this category"}
# it then picks a random value fro mthe array

# updates usage count with - api suffix ie of image type.

# then it sends the image file name and url as a json response
# {"filename" = "", "url" : f"{base_url}/{image_type}/image/{random_image}"}

# /api/random/:type
# converts type to lowercase
# makes list for images
# tries to see if the images folder and type exists with error.

# if images is empty
# {"error: "Picture category not found or there are no images in this category"}

# picks a random imave
# grabs usage type but normal without -api flag

# just send image file as response not url needed, does not use url for this one.


# if just /images/ return {error: "The file category is required"}
# Catch-all route for handling all other undefined routes which was * in the og source code.
# in images/:type?/images/:file?/ it gets the type and makes sure it is lowercased and it also gets the fielname and if type or file are empty it says.
# {error: "The file category is required"}
# {error: "The file name is required"}
# I can make sure with pathlib that a file exists if it does not
# {error: "File not found"}
# however if it does return a path and that is a file then I will return the file object.
# it then updates usage of that image type for some reason.


if __name__ == "__main__":

    uvicorn.run("main:app", port=42069, log_level="debug")
