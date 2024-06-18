from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/role', tags=['role'])


@router.get("/cluster", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=List[str])
async def search_all_cluster(db=Depends(get_db)):
    status_code, result = dbf.get_all_cluster(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_role(Form: sch.post_role_schema, db=Depends(get_db)):
    status_code, result = dbf.post_role(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.role_response)
async def search_role(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_role(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.role_response])
async def search_all_role(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_role(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_role(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_role(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_role(Form: sch.update_role_schema, db=Depends(get_db)):
    status_code, result = dbf.update_role(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
