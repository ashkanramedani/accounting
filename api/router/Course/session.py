from typing import List
from uuid import UUID

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/session', tags=['Sessions'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_session(Form: sch.post_session_schema, db=Depends(get_db)):
    status_code, result = dbf.post_session(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))]) #, response_model=sch.session_response)
async def search_session(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_session(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.session_response])
async def search_all_session(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_session(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{session_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_session(session_id: UUID, sub_course_id: UUID = None, db=Depends(get_db)):
    if not sub_course_id:
        raise HTTPException(status_code=400, detail="subCourse Not Provided")
    status_code, result = dbf.delete_session(db, sub_course_id, [session_id])
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_session(Form: sch.update_session_schema, db=Depends(get_db)):
    status_code, result = dbf.update_session(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result