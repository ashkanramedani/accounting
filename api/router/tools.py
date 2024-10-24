import os
from json import load
from os.path import normpath, dirname, join
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

import db as dbf
import schemas as sch
from lib import logger
from models import get_db

router = APIRouter(tags=["Test"])


@router.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@router.get("/ping", response_model=str)
def ping():
    return "Pong"


@router.get("/api/v1/form/count", response_model=int | str)
async def count(field: str, db=Depends(get_db)):
    status_code, result = dbf.count(db, field)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/api/v1/form/count/help", response_model=List[str])
async def count():
    return ["User", "employee", "student", "Course", "Sub_Course", "Session", "Leave_Request", "Business_Trip", "Remote_Request", "Payment_Method", "Fingerprint_Scanner", "Fingerprint_Scanner_backup", "Teacher_Tardy_report", "Teachers_Report", "Role", "Salary_Policy", "Employee_Salary", "Tag", "Category", "Language", "Course_Type", "Sub_Request", "Session_Cancellation", "Reward_card"]


@router.get("/count", deprecated=True)
async def count(*args, **kwargs):
    logger.warning(f'Deprecated. Use /api/v1/form/count')
    raise HTTPException(status_code=410, detail=f'Deprecated. Use /api/v1/form/count')


@router.get("/testRoute")
async def testRoute(role: str, db=Depends(get_db)):
    return dbf.TestRoute(db, role)


@router.get("/log", include_in_schema=False)
async def Log(log: str = None, limit: int = 100):
    if log:
        try:
            with open(f"./log/{log}") as f:
                Logs = f.readlines()[::-1]
            return Logs[:limit]
        except FileNotFoundError:
            return "<h1>File Not Exist.</h1>"
    return os.listdir("./log")


@router.get("/config", include_in_schema=False)
def config():
    return load(open(join(normpath(f'{dirname(__file__)}/../'), "configs/config.json")))
