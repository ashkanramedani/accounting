from enum import Enum

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from starlette.responses import RedirectResponse

import db as dbf
from db.models import get_db
from lib.log import logger


class log_mode(str, Enum):
    csv = 'csv'
    log = 'log'


router = APIRouter()


@router.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@router.get("/api/v1/form/count", tags=["Ping"])
async def count(field: str, db=Depends(get_db)):
    status_code, result = dbf.count(db, field)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/ping", tags=["Ping"])
def ping():
    return "Pong"


@router.get("/count", tags=["Ping"], deprecated=True)
async def count(field: str, db=Depends(get_db)):
    logger.warning(f'Deprecated. Use /api/v1/form/count')
    if not field:
        raise HTTPException(status_code=400, detail="Field is required")
    status_code, result = dbf.count(db, field)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result
