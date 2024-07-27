from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/salary', tags=['Report'])


@router.get("/permissions/{user_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.permission_response)
async def get_all(user_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.permissions(db, user_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/employee", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Return_Salary])
async def employee_salary(Form: sch.Input, db=Depends(get_db)):
    status_code, result = dbf.employee_salary(db, Form.year, Form.month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/employee/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
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
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/search/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def search_teacher_report(employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
    status_code, result = dbf.get_employee_salary(db, employee_id, year, month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# Form: sch.teacher_salary_report

@router.get("/teacher/courses", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Teacher_course_report])
async def teacher_course(db=Depends(get_db)):
    status_code, result = dbf.teacher_courses(db)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result

@router.get("/teacher/sub_courses/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Teacher_subcourse_report])
async def teacher_sub_course(course_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.teacher_sub_courses(db, course_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
