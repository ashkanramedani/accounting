from enum import Enum
from os.path import normpath, dirname

import pandas as pd
from fastapi import APIRouter, Depends
from starlette.responses import HTMLResponse, RedirectResponse
from typing_extensions import deprecated

import db as dbf
from db.database import get_db
from lib.log import logger


class log_mode(str, Enum):
    csv = 'csv'
    log = 'log'


from starlette.templating import Jinja2Templates

from fastapi import HTTPException

router = APIRouter()


@router.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@router.get("/log", include_in_schema=False, response_class=HTMLResponse)
async def log(mode: log_mode = 'log'):
    templates = Jinja2Templates(directory="./")
    log_path = normpath(f'{dirname(__file__)}/../log/log.{mode}')
    if mode == 'csv':
        pd.read_csv(log_path).to_html("./Tables.html")
        return templates.TemplateResponse("./Tables.html")
        # return "pd.read_csv(log_path).to_dict()"
    with open(log_path, "r") as f:
        log_file = f.read()
    return log_file


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
