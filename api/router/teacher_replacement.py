from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/teacher_replacement', tags=['Teacher Replacement'])


# Teacher replacement

@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_teacher_replacement(Form: sch.post_teacher_replacement_schema, db=Depends(get_db)):
    status_code, result = dbf.post_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_teacher_replacement(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))], response_model=List[sch.teacher_replacement_response])
async def search_all_teacher_replacement(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_teacher_replacement(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_tardy_request(Form: sch.update_teacher_replacement_schema, db=Depends(get_db)):
    status_code, result = dbf.update_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
