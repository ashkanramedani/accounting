from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/user', tags=['User'])


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.export_employee])
async def get_by_role(role: str, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None, db=Depends(get_db)):
    status_code, result = dbf.get_by_role(db, role.lower(), page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
