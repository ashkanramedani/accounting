import json
import uuid
from dataclasses import dataclass
from typing import Literal, Dict
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel
from starlette.responses import JSONResponse

import models.tables as dbm
from db import Set_Status
from models import get_db
import schemas as sch
import db as dbf

router = APIRouter(prefix='/parsian', tags=['gateway'])




@router.post("/create_gateway", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(Form: sch.PaymentRequest, db=Depends(get_db)):
    status_code, result = dbf.parsian_create_gateway(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
    # return RedirectResponse(result)


@router.post("/callback", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(db=Depends(get_db)):
    raise NotImplemented