from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form', tags=['Course_Extension'])


@router.post("/tag/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_tag(Form: sch.post_tag_schema, db=Depends(get_db)):
    status_code, result = dbf.post_tag(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tag/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_tag(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_tag(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tag/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.tag_response])
async def search_all_tag(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_tag(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/tag/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_tag(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_tag(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/tag/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_tag(Form: sch.update_tag_schema, db=Depends(get_db)):
    status_code, result = dbf.update_tag(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/tag/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
def update_tag_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_tag_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# category
@router.post("/category/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_category(Form: sch.post_category_schema, db=Depends(get_db)):
    status_code, result = dbf.post_category(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/category/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_category(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_category(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/category/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.category_response])
async def search_all_category(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_category(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/category/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_category(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_category(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/category/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_category(Form: sch.update_category_schema, db=Depends(get_db)):
    status_code, result = dbf.update_category(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/category/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_category_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_category_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# language

@router.post("/language/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_language(Form: sch.post_language_schema, db=Depends(get_db)):
    status_code, result = dbf.post_language(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/language/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_language(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_language(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/language/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.language_response])
async def search_all_language(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_language(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/language/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_language(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_language(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/language/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_language(Form: sch.update_language_schema, db=Depends(get_db)):
    status_code, result = dbf.update_language(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/language/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_language_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_language_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# course_type
@router.post("/course_type/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_course_type(Form: sch.post_course_type_schema, db=Depends(get_db)):
    status_code, result = dbf.post_course_type(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course_type/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_course_type(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_course_type(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/course_type/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.course_type_response])
async def search_all_course_type(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_course_type(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/course_type/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_course_type(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_course_type(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/course_type/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_course_type(Form: sch.update_course_type_schema, db=Depends(get_db)):
    status_code, result = dbf.update_course_type(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/course_type/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_course_type_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_course_type_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
