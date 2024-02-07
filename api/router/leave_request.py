from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form/leave_request', tags=['Form Leave Forms'])


# leave forms
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_leave_request(Form: sch.post_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_leave_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_leave_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_leave_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_leave_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_leave_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_leave_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_leave_request(Form: sch.update_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_leave_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

