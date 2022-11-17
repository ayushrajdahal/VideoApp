from fastapi import HTTPException, APIRouter
from fastapi.responses import FileResponse
from upload import files

router = APIRouter()

@router.get('/stream-video/{vidname}')       # for streaming a video, given the filename
def stream_video(vidname:str):
    for file in files:
        if file['filename'] == vidname or file['filename'].split():
            return FileResponse(file['path'])

    raise HTTPException(404, detail='Video Not Found')