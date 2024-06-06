from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db
from pydantic import BaseModel

from db.Salary.salary import employee_salary

router = APIRouter(prefix='/api/Dev/test', tags=['test'])

class Input(BaseModel):
    year: int
    month: int


# tardy request
@router.post("/salary", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_student(Form: Input, db=Depends(get_db)):
    status_code, result = employee_salary(db, Form.year, Form.month)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
