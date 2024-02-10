from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/class', tags=['class'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_class(Form: sch.post_class_schema, db=Depends(get_db)):
    status_code, result = dbf.post_class(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_class(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_class(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_class(db=Depends(get_db)):
    status_code, result = dbf.get_all_class(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_class(class_id, db=Depends(get_db)):
    status_code, result = dbf.delete_class(db, class_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_class(Form: sch.update_class_schema, db=Depends(get_db)):
    status_code, result = dbf.update_class(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
