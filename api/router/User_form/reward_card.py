from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/reward_card', tags=['reward_card'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_reward_card(Form: sch.post_reward_card_schema, db=Depends(get_db)):
    status_code, result = dbf.post_reward_card(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.reward_card_response)
async def search_reward_card(form_id: UUID, user: bool = False, db=Depends(get_db)):
    status_code, result = dbf.get_reward_card(db, form_id, user)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.reward_card_response])
async def search_all_reward_card(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_reward_card(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_reward_card(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_reward_card(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_reward_card(Form: sch.update_reward_card_schema, db=Depends(get_db)):
    status_code, result = dbf.update_reward_card(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
