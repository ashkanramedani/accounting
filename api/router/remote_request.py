from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form/remote_request', tags=['Form Remote Request'])



# remote_request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_remote_request(Form: sch.post_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_remote_request_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_remote_request(Form: sch.update_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

