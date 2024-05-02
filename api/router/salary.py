from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db


router = APIRouter(prefix='/api/v1/form/salary', tags=['report'])


@router.get("/employee/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_report(employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID Not provided")
    if not year:
        raise HTTPException(status_code=400, detail="Year Not provided")
    if not month:
        raise HTTPException(status_code=400, detail="Month Not provided")
    if month > 12:
        raise HTTPException(status_code=400, detail="Invalid Month")
    status_code, result = dbf.employee_salary_report(db, employee_id, year, month)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/teacher/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_teacher_report(Form: sch.teacher_salary_report, employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
    raise HTTPException(status_code=503)
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID Not provided")
    if not year:
        raise HTTPException(status_code=400, detail="Year Not provided")
    if not month:
        raise HTTPException(status_code=400, detail="Month Not provided")
    if month > 12:
        raise HTTPException(status_code=400, detail="Invalid Month")
    status_code, result = dbf.teacher_salary_report(db, year, month)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
