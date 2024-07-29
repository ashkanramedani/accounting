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
