from fastapi import HTTPException, UploadFile, Depends, Header, File, APIRouter
import shutil, cv2, os
from pathlib import Path
from datetime import date
from dependencies import valid_content_length

router = APIRouter()
files = []

@router.post("/upload-video/", dependencies=[Depends(valid_content_length)])
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