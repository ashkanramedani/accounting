from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/session_cancellation', tags=['Session Cancellation'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_session_cancellation(Form: sch.post_Session_Cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.post_session_cancellation(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.teacher_tardy_reports_response)
async def search_session_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_session_cancellation(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Session_Cancellation_Response])
async def search_all_session_cancellation(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_session_cancellation(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result

@router.get("/report/{subcourse_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Session_Cancellation_Response])
async def report_session_cancellation(subcourse_id, db=Depends(get_db)):
    status_code, result = dbf.report_session_cancellation(db, subcourse_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result

@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_session_cancellation():
    raise HTTPException(status_code=501, detail="Cancellation form cannot be deleted.")


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_session_cancellation():
    raise HTTPException(status_code=501, detail="Cancellation form cannot be updated.")


@router.put("/updates", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_session_cancellation():
    raise HTTPException(status_code=501, detail="Cancellation form cannot be updated.")


@router.put("/verify/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def verify_session_cancellation():
    raise HTTPException(status_code=501, detail="Cancellation form cannot be verify.")
