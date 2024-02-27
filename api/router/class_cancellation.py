from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/class_cancellation', tags=['Class Cancellation'])


# Class cancellation
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_class_cancellation(Form: sch.post_class_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.post_class_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_class_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_class_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_class_cancellation(db=Depends(get_db)):
    status_code, result = dbf.get_all_class_cancellation_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_class_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_class_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_class_cancellation(Form: sch.update_class_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.update_class_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
