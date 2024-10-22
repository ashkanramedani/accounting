from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from models import get_db

router = APIRouter(prefix='/api/v1/form/zarinpal', tags=['gateway'])


@router.post("/create_gateway", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(Form: sch.PaymentRequest, db=Depends(get_db)):
    status_code, result = dbf.zarinpal_create_gateway(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
    # return RedirectResponse(result)


@router.get("/callback", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def payment_request(Authority: str, Status: Literal["OK", "NOK"], db=Depends(get_db)):
    status_code, result = dbf.zarinpal_callback(db, Status, Authority)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


"""
{
  "data": {
    "wages": [],
    "code": 100,
    "message": "Paid",
    "card_hash": "C257DDFB18DF17F6D9338C5E7C2256D1A6BEEF9FEA1F10DD939F12B30A72B340",
    "card_pan": "628023******8998",
    "ref_id": 59421827101,
    "fee_type": "Merchant",
    "fee": 3500,
    "shaparak_fee": "1200",
    "order_id": "HSA1"
  },
  "errors": []
}
"""
