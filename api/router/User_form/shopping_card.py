from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
import db as dbf
from models import get_db

router = APIRouter(prefix='/api/v1/shopping_card', tags=['Shopping_card'])


# Sub request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_Shopping_card(Form: sch.post_shopping_card_schema, db=Depends(get_db)):
    status_code, result = dbf.post_shopping_card(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch)
async def search_Shopping_card(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_shopping_card(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.shopping_card_response])
async def search_all_Shopping_card(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_shopping_card(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_Shopping_card(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_shopping_card(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_Shopping_card(Form: sch.update_shopping_card_schema, db=Depends(get_db)):
    status_code, result = dbf.update_shopping_card(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/status/{form_id}/{status_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_status(form_id: UUID, status_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.update_shopping_card_status(db, form_id, status_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
