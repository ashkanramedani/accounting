from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form', tags=['course'])


# tardy request
@router.post("/course/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_course(Form: sch.post_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_course(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_course(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_course(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.course_response])
async def search_all_course(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_course(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/course/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_course(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_course(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/course/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_course(Form: sch.update_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_course(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

# - - - - - -  Sub Course ####
@router.post("/subcourse/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_subcourse(Form: sch.post_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_subcourse(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/subcourse/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_subcourse(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_subcourse(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/subcourse/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.sub_course_response])
async def search_all_subcourse(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_subcourse(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/subcourse/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_subcourse(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_subcourse(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/subcourse/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_subcourse(Form: sch.update_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_subcourse(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

# - - - - - -  Session ####
@router.post("/session/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_session(Form: sch.post_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_session(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/session/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_session(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_session(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/session/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.sub_course_response])
async def search_all_session(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_session(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/session/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_session(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_session(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/session/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_session(Form: sch.update_sub_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_session(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

