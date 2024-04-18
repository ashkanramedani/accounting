from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form', tags=['Tag_category'])


@router.post("/tag/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_tag(Form: sch.post_tag_schema, db=Depends(get_db)):
    status_code, result = dbf.post_tag(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tag/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_tag(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_tag(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tag/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.tag_response])
async def search_all_tag(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_tag(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/tag/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_tag(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_tag(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/tag/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_tag(Form: sch.update_tag_schema, db=Depends(get_db)):
    status_code, result = dbf.update_tag(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# tardy request
@router.post("/category/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_category(Form: sch.post_category_schema, db=Depends(get_db)):
    status_code, result = dbf.post_category(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/category/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_category(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_category(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/category/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.category_response])
async def search_all_category(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_category(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/category/delete/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_category(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_category(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/category/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_category(Form: sch.update_category_schema, db=Depends(get_db)):
    status_code, result = dbf.update_category(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
