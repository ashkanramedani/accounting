from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/course_cancellation', tags=['course Cancellation'])


# course cancellation
@router.post("/course", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_course_cancellation(Form: sch.course_cancellation, db=Depends(get_db)):
    status_code, result = dbf.course_cancellation(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/sub_course", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_course_cancellation(Form: sch.sub_course_cancellation, db=Depends(get_db)):
    status_code, result = dbf.sub_course_cancellation(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/session", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_course_cancellation(Form: sch.session_cancellation, db=Depends(get_db)):
    status_code, result = dbf.session_cancellation(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
