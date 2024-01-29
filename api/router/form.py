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

from db import db_form

router = APIRouter(prefix='/api/v1/form', tags=['Form'])

@router.post("/form", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def form(Form: sch.BASE_Leave_Form, db= Depends(get_db)):
   return db_form.post_data(db, Form)

