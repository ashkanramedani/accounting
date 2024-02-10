from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db

router = APIRouter(prefix='/api/v1/form/tardy_request', tags=['Form Tardy Request'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_tardy_request(Form: sch.post_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.post_tardy_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_tardy_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_tardy_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_tardy_request(Form: sch.update_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.update_tardy_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

