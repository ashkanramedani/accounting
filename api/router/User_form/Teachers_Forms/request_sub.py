from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db import Sub_Request
from models import get_db

router = APIRouter(prefix='/api/v1/form/sub_request', tags=['Sub Request'])


# Sub request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_sub_request(Form: sch.post_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Sub_Request.post_sub_request(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch)
async def search_sub_request(form_id, db=Depends(get_db)):
    status_code, result = Sub_Request.get_sub_request(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Sub_request_Response])
async def search_all_sub_request(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = Sub_Request.get_all_sub_request(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/report/{subcourse_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Sub_request_Response])
async def report_sub_request(subcourse_id, db=Depends(get_db)):
    status_code, result = Sub_Request.report_sub_request(db, subcourse_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_sub_request(form_id, db=Depends(get_db)):
    status_code, result = Sub_Request.delete_sub_request(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_sub_request(Form: sch.update_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Sub_Request.update_sub_request(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/updates", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_sub_request(Forms: List[sch.update_Sub_request_schema], db=Depends(get_db)):
    for Form in Forms:
        status_code, result = Sub_Request.update_sub_request(db, Form)
        if status_code not in sch.SUCCESS_STATUS:
            raise HTTPException(status_code=status_code, detail=result)
        return result


@router.put("/verify/{status}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_sub_request(status: sch.CanUpdateStatus, Form: sch.Verify_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Sub_Request.Verify_sub_request(db, Form, status)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_sub_request_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = Sub_Request.update_sub_request_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
