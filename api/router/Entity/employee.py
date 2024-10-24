from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/employee', tags=['Employee'], include_in_schema=False)


@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_employee(Form: sch.post_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.post_employee(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_response)
async def search_employee(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_employee(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.employee_response])
async def search_all_employee(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_employee(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_employee(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_employee(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_employee(Form: sch.update_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.update_employee(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_employee_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_employee_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
