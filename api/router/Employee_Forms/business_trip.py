from typing import List
from uuid import UUID

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/business_trip', tags=['Business Trip'])


# business trip
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_business_trip(Form: sch.post_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.post_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))]) #, response_model=sch.business_trip_response)
async def search_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# @router.post("/report", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
# async def report_business_trip(Form: sch.salary_report, db=Depends(get_db)):
#     status_code, result = dbf.report_business_trip(db, Form)
#     if status_code != 200:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.business_trip_response])
async def search_all_business_trip(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_business_trip_form(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_business_trip(Form: sch.update_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.update_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
