from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db import Sub_Request
from db.models import get_db

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


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=List[sch.teacher_tardy_reports_response])
async def search_all_sub_request(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = Sub_Request.get_all_sub_request(db, page, limit, order)
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


@router.put("/verify", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_sub_request(Form: sch.Verify_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Sub_Request.Verify_sub_request(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
