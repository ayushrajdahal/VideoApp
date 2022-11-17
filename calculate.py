from fastapi import HTTPException, APIRouter

router = APIRouter()

@router.get('/calculate-charges')
def calculate_charge(vid_size:int, length:float, filetype:str):
    
    # file validation

    if filetype.lower() not in ('mkv', 'mp4'):
        raise HTTPException(415, detail='Invalid File Type')

    if vid_size>1e9:            # raises an error if size > 1 GB
        raise HTTPException(413, detail="file too large")

    # charge calculation

    totalcharge = 0
    
    if vid_size <= 500_000_000: # charges $5 for <= 500MB, $12.5 for more
        totalcharge+=5
    else:
        totalcharge+=12.5
    
    if length <= 6*60 + 18:     # charges additional $12.5 for <= 6m 18s, $20 for more
        totalcharge += 12.5
    else:
        totalcharge += 20
    
    return {'Charge':totalcharge}