from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/payment_method', tags=['payment_method'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_payment_method(Form: sch.post_payment_method_schema, db=Depends(get_db)):
    status_code, result = dbf.post_payment_method(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=sch.payment_method_response)
async def search_payment_method(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_payment_method(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.payment_method_response])
async def search_all_payment_method(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_payment_method(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_payment_method(payment_method_id, db=Depends(get_db)):
    status_code, result = dbf.delete_payment_method(db, payment_method_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_payment_method(Form: sch.update_payment_method_schema, db=Depends(get_db)):
    status_code, result = dbf.update_payment_method(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
