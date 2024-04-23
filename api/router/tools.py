from fastapi import APIRouter
import pandas as pd
from typing import List

from starlette.responses import HTMLResponse

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from os.path import normpath, dirname
import db as dbf
import schemas as sch
from db.database import get_db



from enum import Enum


class log_mode(str, Enum):
    csv = 'csv'
    log = 'log'


# from prettytable import PrettyTable

# def create_table(log_path):
#     a = open(log_path, 'r')
#     a = a.readlines()
#     lables = ["time", "types", "func", "message"]
#
#     # headers for table
#     t = PrettyTable([l1[0], l1[1]])
#
#     # Adding the data
#     for i in range(1, len(a)) :
#         t.add_row(a[i].split(','))
#
#     return t.get_html_string()
#     html_file = open('Tablee.html', 'w')
#     html_file = html_file.write(code)
from starlette.templating import Jinja2Templates

from fastapi import HTTPException, Request

router = APIRouter()
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
