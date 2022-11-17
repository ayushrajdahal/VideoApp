from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import cv2
from datetime import date
import os, shutil, uvicorn, tempfile
from typing import Optional
from pydantic import BaseModel
from dependencies import valid_content_length
import stream, upload, listvid, calculate

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