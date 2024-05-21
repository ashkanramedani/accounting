from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/teacher_replacement', tags=['Teacher Replacement'])


# Teacher replacement

@router.post("/session", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def session_teacher_replacement(Form: sch.session_teacher_replacement, db=Depends(get_db)):
    status_code, result = dbf.session_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# sub_course

@router.post("/subcourse", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def subcourse_teacher_replacement(Form: sch.subcourse_teacher_replacement, db=Depends(get_db)):
    status_code, result = dbf.sub_course_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result