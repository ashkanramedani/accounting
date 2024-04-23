from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/sub_course', tags=['course'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_subcourse(Form: sch.post_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_subcourse(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.sub_course_response)
async def search_subcourse(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_subcourse(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.sub_course_response])
async def search_all_subcourse(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_subcourse(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}") #, dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_subcourse(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_subcourse(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_subcourse(Form: sch.update_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_subcourse(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

