from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse

import db as dbf
import schemas as sch
from db.models import get_db
from lib import logger

router = APIRouter()


@router.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@router.get("/api/v1/form/count", tags=["Test"], response_model=int | str)
async def count(field: str, db=Depends(get_db)):
    status_code, result = dbf.count(db, field)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/ping", tags=["Test"], response_model=str)
def ping():
    return "Pong"


@router.get("/api/v1/form/count/help", tags=["Test"], response_model=List[str])
async def count():
    return ["User", "employee", "student", "Course", "Sub_Course", "Session", "Leave_Request", "Business_Trip", "Remote_Request", "Payment_Method", "Fingerprint_Scanner", "Fingerprint_Scanner_backup", "Teacher_Tardy_report", "Teachers_Report", "Role", "Salary_Policy", "Employee_Salary", "Tag", "Category", "Language", "Course_Type", "Sub_Request", "Session_Cancellation"]


# return ["User", "Course", "Sub_Course", "Session", "Leave_Request", "Business_Trip", "Remote_Request", "Payment_Method", "Fingerprint_Scanner", "Fingerprint_Scanner_backup", "Teacher_Tardy_report", "Teachers_Report", "Survey", "Question", "Response", "Role", "Salary_Policy", "Employee_Salary", "Tag", "Category", "Language", "Course_Type", "Status", "Sub_Request", "Session_Cancellation", "Reassign_Instructor"]


@router.get("/count", tags=["Test"], deprecated=True)
async def count(*args, **kwargs):
    logger.warning(f'Deprecated. Use /api/v1/form/count')
    raise HTTPException(status_code=410, detail=f'Deprecated. Use /api/v1/form/count')


def conv(item: int | float | sch.three_Option | sch.four_Option):
    if isinstance(item, int) or isinstance(item, float):
        return f'IorF: {item}'
    else:
        return f'ENUM: {item.value}'


@router.post("/testRoute", tags=["Test"])
async def testRoute(Form: sch.teacher_salary_DropDowns, db=Depends(get_db)):
    return {k: conv(v) for k, v in Form.__dict__.items()}
