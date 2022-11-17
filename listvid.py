from pydantic import BaseModel
from typing import Optional
from datetime import date
from upload import files
from fastapi import APIRouter

router = APIRouter()

class ListConditions(BaseModel):                # for list_videos endpoint
    minLength:Optional[float]=0                 # minimum video length
    maxLength:Optional[float]=1e9               # max video length
    dateFrom:Optional[date]=date(1970,1,1)      # earliest date
    dateTill:Optional[date]=date.today()        # latest date


@router.post('/list-videos/')
def list_videos(conds:ListConditions):          # for listing all videos that satisfy the given parameters
    output_list = {}
    index_num = 1
    for file in files:
        if file['duration'] >= conds.minLength and file['duration'] <= conds.maxLength and file['date_added'] >= conds.dateFrom and file['date_added'] <= conds.dateTill:
            output_list[index_num] = file
            index_num+=1

    return [output_list[index]['filename'] for index in output_list]