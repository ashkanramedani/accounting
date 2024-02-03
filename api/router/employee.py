# import logging
# from uuid import UUID
# import sqlalchemy.sql.expression as sse
# from datetime import datetime, timedelta
# from api.db import db_employee
# from typing import Optional, List, Dict, Any, Union, Annotated
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel
# from api.lib import Hash, Massenger, Tools
# # from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token

import schemas as sch
import db.models as dbm
from fastapi import APIRouter, Query, Body, Path, Depends, Response, HTTPException, status, UploadFile, File
from db.database import get_db
from fastapi_limiter.depends import RateLimiter
import db as dbf


router = APIRouter(prefix='/api/v1/employee', tags=['Employee'])


@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_employee(Form: sch.post_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.post_employee(db, Form)
    return HTTPException(status_code=status_code, detail=result)


@router.get("/search/{employee_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_employee(employee_id, db=Depends(get_db)):
    status_code, result = dbf.get_employee(db, employee_id)
    return HTTPException(status_code=status_code, detail=result)


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_employee(db=Depends(get_db)):
    status_code, result = dbf.get_all_employee(db)
    return HTTPException(status_code=status_code, detail=result)


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_employee(Form: sch.delete_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.delete_employee(db, Form)
    return HTTPException(status_code=status_code, detail=result)


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_employee(Form: sch.update_employee_schema, db=Depends(get_db)):
    status_code, result = dbf.update_employee(db, Form)
    return HTTPException(status_code=status_code, detail=result)
