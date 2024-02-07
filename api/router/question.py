from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form/question', tags=['question'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_question(Form: sch.post_questions_schema, db=Depends(get_db)):
    status_code, result = dbf.post_question(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_question(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_question(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_all_question(db=Depends(get_db)):
    status_code, result = dbf.get_all_question(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_question(question_id, db=Depends(get_db)):
    status_code, result = dbf.delete_question(db, question_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_question(Form: sch.update_questions_schema, db=Depends(get_db)):
    status_code, result = dbf.update_question(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

