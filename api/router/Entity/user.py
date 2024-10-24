from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/user', tags=['User'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_user(Form: sch.post_user_schema, db=Depends(get_db)):
    status_code, result = dbf.post_user(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.user_response)
async def search_user(form_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.get_user(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.user_response])
async def search_all_user(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_user(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search_role/{role}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.user_response])
async def get_by_role(role: str, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None, db=Depends(get_db)):
    status_code, result = dbf.get_by_role(db, role.lower(), page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_user(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_user(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_user(Form: sch.update_user_schema, db=Depends(get_db)):
    status_code, result = dbf.update_user(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_user_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_user_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/count")
async def update_user_status(role: str, db=Depends(get_db)):
    status_code, result = dbf.get_by_role(db, role, 0)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return len(result)
