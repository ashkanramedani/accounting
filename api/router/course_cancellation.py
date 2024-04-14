from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/course_cancellation', tags=['course Cancellation'])


# class cancellation
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_course_cancellation(Form: sch.post_course_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.post_course_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_course_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_course_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

# @router.post("/report", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# async def report_course_cancellation(Form: sch.teacher_report, db=Depends(get_db)):
#     status_code, result = dbf.report_course_cancellation(db, Form)
#     if status_code != 200:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result

@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.course_cancellation_response])
async def search_all_course_cancellation(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_course_cancellation_form(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_course_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_course_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_course_cancellation(Form: sch.update_course_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.update_course_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
