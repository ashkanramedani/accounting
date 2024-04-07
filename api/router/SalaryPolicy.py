from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/SalaryPolicy', tags=['SalaryPolicy'])

@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_SalaryPolicy(Form: sch.post_SalaryPolicy_schema, db=Depends(get_db)):
    status_code, result = dbf.post_SalaryPolicy(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_SalaryPolicy(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_SalaryPolicy(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_SalaryPolicy(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_SalaryPolicy(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_SalaryPolicy(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_SalaryPolicy(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_SalaryPolicy(Form: sch.update_SalaryPolicy_schema, db=Depends(get_db)):
    status_code, result = dbf.update_SalaryPolicy(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
