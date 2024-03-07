from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/survey', tags=['survey'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_survey(Form: sch.post_survey_schema, db=Depends(get_db)):
    status_code, result = dbf.post_survey(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=sch.survey_response)
async def search_survey(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_survey(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.survey_response])
async def search_all_survey(db=Depends(get_db), page: int = 1, limit: int = 10):
    status_code, result = dbf.get_all_survey(db, page, limit)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_survey(survey_id, db=Depends(get_db)):
    status_code, result = dbf.delete_survey(db, survey_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_survey(Form: sch.update_survey_schema, db=Depends(get_db)):
    raise HTTPException(status_code=404, detail="Not Found")
    # status_code, result = dbf.update_survey(db, Form)
    # if status_code != 200:
    #     raise HTTPException(status_code=status_code, detail=result)
    # return result
