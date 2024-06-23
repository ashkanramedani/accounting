from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel

import schemas as sch
from db.Salary.salary import employee_salary
from db.models import get_db

router = APIRouter(prefix='/api/Dev/test', tags=['Test'])


class Input(BaseModel):
    year: int
    month: int


class Return_Salary(sch.export_employee):
    Does_Have_Salary_Record: bool
    role: Optional[Any] = None

    class Config:
        orm_mode = True


# tardy request
@router.post("/salary", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[Return_Salary])
async def add_student(Form: Input, db=Depends(get_db)):
    status_code, result = employee_salary(db, Form.year, Form.month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
