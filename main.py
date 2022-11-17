from fastapi import FastAPI
import os,uvicorn
from video_operations import stream, upload, listvid, calculate

app = FastAPI()


app.include_router(
    upload.router,
    tags=['upload']
    )
app.include_router(
    listvid.router,
    tags=['video operations']
    )
app.include_router(
    calculate.router,
    tags=['video operations']
    )
app.include_router(
    stream.router,
    tags=['extra features']
    )

if not os.path.exists('./static'):              # here's where the videos get stored
    os.mkdir('static')


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)