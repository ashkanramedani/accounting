from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form/student', tags=['Student'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_student(Form: sch.post_student_schema, db=Depends(get_db)):
    status_code, result = dbf.post_student(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_student(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_student(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_student(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_student(student_id, db=Depends(get_db)):
    status_code, result = dbf.delete_student(db, student_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_student(Form: sch.update_student_schema, db=Depends(get_db)):
    status_code, result = dbf.update_student(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

