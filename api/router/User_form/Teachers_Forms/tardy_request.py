from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/tardy_request', tags=['Tardy Request'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_tardy_request(Form: sch.post_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.post_tardy_request(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.teacher_tardy_reports_response)
async def search_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_tardy_request(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.teacher_tardy_reports_response])
async def search_all_tardy_request(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_tardy_request(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/report/{subcourse_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.teacher_tardy_reports_response])
async def report_tardy_request(subcourse_id, db=Depends(get_db)):
    status_code, result = dbf.report_tardy_request(db, subcourse_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_tardy_request(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_tardy_request(Form: sch.update_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.update_tardy_request(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/updates", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_tardy_request(Forms: List[sch.update_teacher_tardy_reports_schema], db=Depends(get_db)):
    for Form in Forms:
        status_code, result = dbf.update_tardy_request(db, Form)
        if status_code not in sch.SUCCESS_STATUS:
            raise HTTPException(status_code=status_code, detail=result)
        return result


@router.put("/verify/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def verify_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.verify_tardy_request(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_tardy_request_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
