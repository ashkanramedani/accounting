from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/employee', tags=['Employee'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_employee(Form: sch.post_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.post_employee(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{employee_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_employee(employee_id, db=Depends(get_db)):
    status_code, result = dbf.get_employee(db, employee_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.employee_response])
async def search_all_employee(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_employee(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_employee(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_employee(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_employee(Form: sch.update_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.update_employee(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
