import logging
import schemas as sch
import db.models as dbm
import sqlalchemy.sql.expression as sse
from datetime import datetime, timedelta
from uuid import UUID
from typing import Optional, List, Dict, Any, Union, Annotated
from fastapi import APIRouter, Query, Body, Path, Depends, Response, HTTPException, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db.database import get_db
# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
from fastapi_limiter.depends import RateLimiter
from lib.hash import Hash
from lib.functions import Massenger, Tools

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

from db import db_employee

router = APIRouter(prefix='/api/v1/employee', tags=['Employee'])

@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_employee(employee: sch.BASE_Employee, response: Response, db= Depends(get_db)):
    try:
        OBJ = Models.Employee(
                name=employee.name,
                last_name=employee.last_name,
                job_title=employee.job_title)

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200
    except Exception as error:
        logger.error(error)
        return 500


@router.post("/search")
async def search_employee(employee_id: int, db= Depends(get_db)):
    res = db.query(Models.Employee).filter(Models.Employee.id == employee_id).all()

    logger.info(res)
    if not res:
        return {"status_code": 200, "res": "NotFound"}
    return {"status_code": 200, "res": res}
