from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import cv2
from datetime import date
import os, shutil, uvicorn, tempfile
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

files = []
# tempfolder = tempfile.TemporaryDirectory()

class ListConditions(BaseModel):                # for list_videos endpoint
    minLength:Optional[float]=0                 # minimum video length
    maxLength:Optional[float]=1e9              # max video length
    dateFrom:Optional[date]=date(1970,1,1)     # earliest 
    dateTill:Optional[date]=date.today()



async def valid_content_length(content_length: int = Header(..., lt=1_000_000_001)): # only allows file upload of upto 1 GB
    return content_length




@app.post("/upload-video", dependencies=[Depends(valid_content_length)])
def create_file(file: UploadFile = File(...)):

    if file.filename.split('.')[1] not in ('mkv', 'mp4'):       # file type check
        raise HTTPException(415, detail='Invalid File Type')
    

    videopath = os.path.join(Path('./static/'), file.filename)
    file_object = file.file

    upload_folder = open(videopath, 'wb+')                 # creating empty file to copy the file_object to
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    

    cap = cv2.VideoCapture(videopath, cv2.CAP_FFMPEG)    # gets video duration using OpenCV
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps


    files.append({
    "filename": file.filename, 
    "type": file.filename.split('.')[1],
    "path": videopath,
    "duration": duration,
    "date_added": date.today(),
    "size": os.stat(videopath).st_size
    })
    return {'Success': 'File uploaded succesfully'}


@app.post('/list-videos')
def list_videos(conds:ListConditions):          # for listing all videos that satisfy the given parameters
    output_list = {}
    index_num = 1
    for file in files:
        if file['duration'] >= conds.minLength and file['duration'] <= conds.maxLength and file['date_added'] >= conds.dateFrom and file['date_added'] <= conds.dateTill:
            output_list[index_num] = file
            index_num+=1

    return [output_list[index]['filename'] for index in output_list]



@app.get('/calculate-charges')
def calculate_charge(vid_size:int, length:float, filetype:str):
    
    # validation

    if filetype.lower() not in ('mkv', 'mp4'):
        raise HTTPException(415, detail='Invalid File Type')

    if vid_size>1e9:        # raises an error if size > 1 GB
        raise HTTPException(413, detail="file too large")

    # charge calculation

    totalcharge = 0
    
    if vid_size <= 500_000_000: #charges $5 for <= 500MB, $12.5 for more
        totalcharge+=5
    else:
        totalcharge+=12.5
    
    if length <= 6*60 + 18:     # charges additional $12.5 for <= 6m 18s, $20 for more
        totalcharge += 12.5
    else:
        totalcharge += 20
    
    return {'Charge':totalcharge}


@app.get('/stream-video')       # for streaming a video, given the filename
def stream_video(vidname:str):
    for file in files:
        if file['filename'] == vidname or file['filename'].split():
            return FileResponse(file['path'])

    raise HTTPException(404, detail='Video Not Found')


if __name__ == "__main__":
    uvicorn.run("videoproject:app", host="127.0.0.1", port=5000, reload=True)