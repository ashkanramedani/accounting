from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/parsian', tags=['gateway'])


@router.post("/create_gateway", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(Form: sch.PaymentRequest, db=Depends(get_db)):
    status_code, result = dbf.parsian_create_gateway(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
    # return RedirectResponse(result)


@router.post("/callback", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(Form: sch.parsian_callBack, db=Depends(get_db)):
    status_code, result = dbf.parsian_callback(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
