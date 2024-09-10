import pathlib

import uvicorn
from fastapi import FastAPI

app = FastAPI()

current_directory = pathlib.Path(__file__).absolute().parent
images_directory = pathlib.Path(str(current_directory) + "/images")

if __name__ == "__main__":

    uvicorn.run("main:app", port=42069, log_level="debug")
