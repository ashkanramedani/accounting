from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/session', tags=['Sessions'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_session(Form: sch.post_session_schema, db=Depends(get_db)):
    status_code, result = dbf.post_session(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.session_response)
async def search_session(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_session(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.session_response])
async def search_all_session(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_session(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/sub_party", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.session_response])
async def search_all_session(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_sub_party(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{session_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_session(session_id: UUID, sub_course_id: UUID = None, db=Depends(get_db)):
    if not sub_course_id:
        raise HTTPException(status_code=400, detail="subCourse Not Provided")
    status_code, result = dbf.delete_session(db, sub_course_id, [session_id])
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_session(Form: sch.update_session_schema, db=Depends(get_db)):
    status_code, result = dbf.update_session(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
