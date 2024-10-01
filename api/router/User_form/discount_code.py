from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/discount_code', tags=['discount_code'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_discount_code(Form: sch.post_discount_code_schema, db=Depends(get_db)):
    status_code, result = dbf.post_discount_code(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.discount_code_response)
async def search_discount_code(form_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.get_discount_code(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.discount_code_response])
async def search_all_discount_code(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_discount_code(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_discount_code(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_discount_code(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_discount_code(Form: sch.update_discount_code_schema, db=Depends(get_db)):
    status_code, result = dbf.update_discount_code(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_discount_code_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/apply_code", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def apply_discount_code(Form: sch.apply_code, db=Depends(get_db)):
    status_code, result = dbf.apply_discount_code(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
