from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/sub_course', tags=['Sub Course'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_subcourse(Form: sch.post_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_subcourse(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/teacher_subcourse/{user_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=Union[sch.sub_course_response_notJoined, List[sch.sub_course_response_notJoined]])
async def search_teacher_subcourse(user_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.get_teacher_subcourse(db, user_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  #, response_model=Union[sch.sub_course_response_notJoined, List[sch.sub_course_response_notJoined]])
async def search_subcourse(form_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.get_subcourse(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.sub_course_response])
async def search_all_subcourse(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_subcourse(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.sub_course_response])
async def search_subcourse_by_course_id(course_id: UUID, page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc", SortKey: str = None, db=Depends(get_db)):
    status_code, result = dbf.get_sub_courses_for_course(db, course_id, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{sub_course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_subcourse(sub_course_id: UUID, course_id: UUID = None, db=Depends(get_db)):
    status_code, result = dbf.delete_subcourse(db, course_id, [sub_course_id])
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_subcourse(Form: sch.update_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_subcourse(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{sub_course_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_subcourse_status(sub_course_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_subcourse_status(db, sub_course_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
