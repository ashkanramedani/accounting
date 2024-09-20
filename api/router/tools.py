import json
import os
from typing import List
from os.path import normpath, dirname, join
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from json import load

import db as dbf
import schemas as sch
from models import get_db
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
    return ["User", "employee", "student", "Course", "Sub_Course", "Session", "Leave_Request", "Business_Trip", "Remote_Request", "Payment_Method", "Fingerprint_Scanner", "Fingerprint_Scanner_backup", "Teacher_Tardy_report", "Teachers_Report", "Role", "Salary_Policy", "Employee_Salary", "Tag", "Category", "Language", "Course_Type", "Sub_Request", "Session_Cancellation", "Reward_card"]


@router.get("/count", tags=["Test"], deprecated=True)
async def count(*args, **kwargs):
    logger.warning(f'Deprecated. Use /api/v1/form/count')
    raise HTTPException(status_code=410, detail=f'Deprecated. Use /api/v1/form/count')


@router.get("/testRoute", tags=["Test"])
async def testRoute(db=Depends(get_db)):
    return dbf.TestRoute(db)


@router.get("/log", tags=["Test"], include_in_schema=False)
async def Log(log: str = None, limit: int = 100):
    if log:
        try:
            with open(f"./log/{log}") as f:
                Logs = f.readlines()[::-1]
            return Logs[:limit]
        except FileNotFoundError:
            return "File Not Exist."
    return os.listdir("./log")


@router.get("/config", tags=["Test"], include_in_schema=False)
def config():
    return load(open(join(normpath(f'{dirname(__file__)}/../'), "configs/config.json")))
