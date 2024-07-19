import io
from typing import List
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from fastapi import HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db
from lib.Date_Time import generate_month_interval

router = APIRouter(prefix='/api/v1/form/fingerprint_scanner', tags=['Fingerprint_scanner'])


# leave forms
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def add_fingerprint_scanner(Form: sch.post_fingerprint_scanner_schema, db=Depends(get_db)):
    status_code, result = dbf.post_fingerprint_scanner(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


async def LoadFile(file: UploadFile):
    try:
        filename = file.filename
        content = await file.read()
        if filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
        elif filename.endswith('.csv') or filename.endswith('.txt'):
            try:
                decoded_content = content.decode("utf-16-le")  # Decode with UTF-16LE encoding
            except UnicodeDecodeError:
                decoded_content = content.decode("utf-8")  # Decode with UTF-8 encoding

            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded_content))
            else:
                df = pd.read_csv(io.StringIO(decoded_content), sep="\t")
        else:
            return 500, "Unsupported file format"
        try:
            try:
                df.columns = ["No", "TMNo", "EnNo", "Name", "GMNo", "Mode", "In_Out", "Antipass", "ProxyWork", "DateTime"]
                df = df.drop('No', axis=1)
            except ValueError:
                df.columns = ["TMNo", "EnNo", "Name", "GMNo", "Mode", "In_Out", "Antipass", "ProxyWork", "DateTime"]

            df = df.drop('Name', axis=1)
            df["DateTime"] = pd.to_datetime(df["DateTime"], errors='coerce').dt.floor('min')
            df = df.sort_values(by="DateTime").drop_duplicates()
            df.rename(columns={"In/Out": "In_Out"}, inplace=True)
            return 200, df
        except pd.errors.ParserError:
            return 400, f"Error parsing the CSV."
    except Exception as e:
        return 500, f'{e.__class__.__name__}: {e.args}'


@router.post("/bulk_add/{created_by}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def bulk_add_fingerprint_scanner(created_by: UUID, db=Depends(get_db), file: UploadFile = File(...)):
    status_code, Data = await LoadFile(file)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=Data)
    status_code, result = dbf.post_bulk_fingerprint_scanner(db, created_by, Data)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.fingerprint_scanner_response)
async def search_fingerprint_scanner(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_fingerprint_scanner(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.fingerprint_scanner_response])
async def search_all_fingerprint_scanner(db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 100, order: sch.Sort_Order = "desc", SortKey: str = None):
    status_code, result = dbf.get_all_fingerprint_scanner(db, page, limit, order, SortKey)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/report/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.FingerPrint_report)
async def report_fingerprint_scanner(employee_id: int | UUID, year: int, month: int, db=Depends(get_db)):
    start, end = generate_month_interval(year, month, include_nex_month_fist_day=False)
    status_code, result = dbf.report_fingerprint_scanner(db, employee_id, start, end)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_fingerprint_scanner(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_fingerprint_scanner(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_fingerprint_scanner(Form: sch.update_fingerprint_scanner_schema, db=Depends(get_db)):
    status_code, result = dbf.update_fingerprint_scanner(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
