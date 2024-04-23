from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/response', tags=['response'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_response(Form: sch.post_response_schema, db=Depends(get_db)):
    status_code, result = dbf.post_response(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.response_response)
async def search_response(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_response(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.response_response])
async def search_all_response(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_response(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_response(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_response(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_response(Form: sch.update_response_schema, db=Depends(get_db)):
    raise HTTPException(status_code=410, detail=status.HTTP_410_GONE)
    # status_code, result = dbf.update_response(db, Form)
    # if status_code != 200:
    #     raise HTTPException(status_code=status_code, detail=result)
    # return result
