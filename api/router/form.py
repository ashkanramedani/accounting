from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form', tags=['Form'])


@router.post("/leave_request/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_leave_request(Form: sch.post_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_leave_request(db, Form)
    return HTTPException(status_code=status_code, detail=result)


@router.get("/leave_request/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_leave_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_leave_request(db, form_id)
    return HTTPException(status_code=status_code, detail=result)


@router.get("/leave_request/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_leave_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    return HTTPException(status_code=status_code, detail=result)


@router.delete("/leave_request/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_leave_request(Form: sch.delete_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.delete_leave_request(db, Form)
    return HTTPException(status_code=status_code, detail=result)


@router.put("/leave_request/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_leave_request(Form: sch.update_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_leave_request(db, Form)
    return HTTPException(status_code=status_code, detail=result)
