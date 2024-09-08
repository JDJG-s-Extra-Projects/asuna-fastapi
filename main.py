import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":

    uvicorn.run("main:app", port=2312, log_level="debug")
