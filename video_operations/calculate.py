from fastapi import HTTPException, APIRouter
from pydantic import BaseModel


router = APIRouter()

class CalculateInputs(BaseModel):
    vidsize:int
    vidlength:float
    vidtype:str

@router.post('/calculate-charges')
def calculate_charge(calcinput:CalculateInputs):
    
    # file validation

    if calcinput.vidtype.lower() not in ('mkv', 'mp4'):
        raise HTTPException(415, detail='Invalid File Type')

    if calcinput.vidsize>1e9:            # raises an error if size > 1 GB
        raise HTTPException(413, detail="file too large")

    # charge calculation

    totalcharge = 0
    
    if calcinput.vidsize <= 500_000_000: # charges $5 for <= 500MB, $12.5 for more
        totalcharge+=5
    else:
        totalcharge+=12.5
    
    if calcinput.vidlength <= 6*60 + 18:     # charges additional $12.5 for <= 6m 18s, $20 for more
        totalcharge += 12.5
    else:
        totalcharge += 20
    
    return {'Charge':totalcharge}