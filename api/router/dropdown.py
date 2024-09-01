from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/dropdown', tags=['Drop Down'])


@router.get("/user", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.user_dropdown])
async def employee_dropdown(db=Depends(get_db), order: sch.Sort_Order = "desc", SortKey: str = "name", employee: bool = True):
    status_code, result = dbf.user_dropdown(db, order, SortKey, is_employee=employee)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
