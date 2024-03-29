from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.database import get_db
from typing import Annotated
from fastapi import File, UploadFile, Body


router = APIRouter(prefix='/api/v1/form/fingerprint_scanner', tags=['fingerprint_scanner'])


# leave forms
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_fingerprint_scanner(Form: sch.post_fingerprint_scanner_schema, db=Depends(get_db)):
    status_code, result = dbf.post_fingerprint_scanner(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.post("/bulk_add/{created_by}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def bulk_add_fingerprint_scanner(created_by: UUID, db=Depends(get_db), file: UploadFile = File(...)):
    status_code, result = dbf.post_bulk_fingerprint_scanner(db, created_by, file)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_fingerprint_scanner(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_fingerprint_scanner(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_fingerprint_scanner(db=Depends(get_db), page: sch.PositiveInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_fingerprint_scanner(db, page, limit, order)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_fingerprint_scanner(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_fingerprint_scanner(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_fingerprint_scanner(Form: sch.update_fingerprint_scanner_schema, db=Depends(get_db)):
    status_code, result = dbf.update_fingerprint_scanner(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
