from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form', tags=['Course Extension'])


# course_type
@router.post("/course_type/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_course_type(Form: sch.post_course_type_schema, db=Depends(get_db)):
    status_code, result = dbf.post_course_type(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course_type/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_course_type(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_course_type(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course_type/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.course_type_response])
async def search_all_course_type(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_course_type(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/course_type/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_course_type(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_course_type(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/course_type/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_course_type(Form: sch.update_course_type_schema, db=Depends(get_db)):
    status_code, result = dbf.update_course_type(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/course_type/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_course_type_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_course_type_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
