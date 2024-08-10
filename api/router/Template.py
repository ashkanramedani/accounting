from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db import Template
from db.models import get_db

router = APIRouter(prefix='/api/v1/template', tags=['Template_form'])


# Sub request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_template(Form: sch.post_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Template.post_template(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch)
async def search_template(form_id, db=Depends(get_db)):
    status_code, result = Template.get_template(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.template_response])
async def search_all_template(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = Template.get_all_template(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_template(form_id, db=Depends(get_db)):
    status_code, result = Template.delete_template(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_template(Form: sch.update_Sub_request_schema, db=Depends(get_db)):
    status_code, result = Template.update_template(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/updates", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_template(Forms: List[sch.update_Sub_request_schema], db=Depends(get_db)):
    for Form in Forms:
        status_code, result = Template.update_template(db, Form)
        if status_code not in sch.SUCCESS_STATUS:
            raise HTTPException(status_code=status_code, detail=result)
        return result
