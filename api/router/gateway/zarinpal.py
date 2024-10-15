import json
from dataclasses import dataclass
from typing import Literal, Dict
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel
from starlette.responses import JSONResponse


from fastapi.responses import RedirectResponse

import models.tables as dbm
from db import Set_Status
from models import get_db
import schemas as sch
import db as dbf

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


STATUS = {
    "-9": {
        "EN": "Validation error",
        "FA": "خطای اعتبار سنجی - 1- مرچنت کد داخل تنظیمات وارد نشده باشد - 2 آدرس بازگشت (callbackurl) وارد نشده باشد - 3 توضیحات (description ) وارد نشده باشد و یا از حد مجاز 500 کارکتر بیشتر باشد - 4 مبلغ پرداختی کمتر یا بیشتر از حد مجاز"
    },
    "-10": {
        "EN": "Terminal is not valid, please check merchant_id or ip address.",
        "FA": "ای پی یا مرچنت كد پذیرنده صحیح نیست."
    },
    "-11": {
        "EN": "Terminal is not active, please contact our support team.",
        "FA": "مرچنت کد فعال نیست، پذیرنده مشکل خود را به امور مشتریان زرین‌پال ارجاع دهد."
    },
    "-12": {
        "EN": "To many attempts, please try again later.",
        "FA": "تلاش بیش از دفعات مجاز در یک بازه زمانی کوتاه به امور مشتریان زرین پال اطلاع دهید."
    },
    "-15": {
        "EN": "Terminal user is suspend : (please contact our support team).",
        "FA": "درگاه پرداخت به حالت تعلیق در آمده است، پذیرنده مشکل خود را به امور مشتریان زرین‌پال ارجاع دهد."
    },
    "-16": {
        "EN": "Terminal user level is not valid : ( please contact our support team).",
        "FA": "سطح تایید پذیرنده پایین تر از سطح نقره ای است."
    },
    "-17": {
        "EN": "Terminal user level is not valid : ( please contact our support team).",
        "FA": "محدودیت پذیرنده در سطح آبی"
    },
    "100": {
        "EN": "Success",
        "FA": "عملیات موفق"
    },
    "-30": {
        "EN": "Terminal do not allow to accept floating wages.",
        "FA": "پذیرنده اجازه دسترسی به سرویس تسویه اشتراکی شناور را ندارد."
    },
    "-31": {
        "EN": "Terminal do not allow to accept wages, please add default bank account in panel.",
        "FA": "حساب بانکی تسویه را به پنل اضافه کنید. مقادیر وارد شده برای تسهیم درست نیست. پذیرنده جهت استفاده از خدمات سرویس تسویه اشتراکی شناور، باید حساب بانکی معتبری به پنل کاربری خود اضافه نماید."
    },
    "-32": {
        "EN": "Wages is not valid, Total wages(floating) has been overload max amount.",
        "FA": "مبلغ وارد شده از مبلغ کل تراکنش بیشتر است."
    },
    "-33": {
        "EN": "Wages floating is not valid.",
        "FA": "درصدهای وارد شده صحیح نیست."
    },
    "-34": {
        "EN": "Wages is not valid, Total wages(fixed) has been overload max amount.",
        "FA": "مبلغ وارد شده از مبلغ کل تراکنش بیشتر است."
    },
    "-35": {
        "EN": "Wages is not valid, Total wages(floating) has been reached the limit in max parts.",
        "FA": "تعداد افراد دریافت کننده تسهیم بیش از حد مجاز است."
    },
    "-36": {
        "EN": "The minimum amount for wages(floating) should be 10,000 Rials",
        "FA": "حداقل مبلغ جهت تسهیم باید ۱۰۰۰۰ ریال باشد"
    },
    "-37": {
        "EN": "One or more iban entered for wages(floating) from the bank side are inactive.",
        "FA": "یک یا چند شماره شبای وارد شده برای تسهیم از سمت بانک غیر فعال است."
    },
    "-38": {
        "EN": "Wages need to set Iban in shaparak.",
        "FA": "خطا٬عدم تعریف صحیح شبا٬لطفا دقایقی دیگر تلاش کنید."
    },
    "-39": {
        "EN": "Wages have a error!",
        "FA": "خطایی رخ داده است به امور مشتریان زرین پال اطلاع دهید"
    },
    "-40": {
        "EN": "Invalid extra params, expire_in is not valid.",
        "FA": ""
    },
    "-41": {
        "EN": "Maximum amount is 100,000,000 tomans.",
        "FA": "حداکثر مبلغ پرداختی ۱۰۰ میلیون تومان است"
    },
    "-50": {
        "EN": "Session is not valid, amounts values is not the same.",
        "FA": "مبلغ پرداخت شده با مقدار مبلغ ارسالی در متد وریفای متفاوت است."
    },
    "-51": {
        "EN": "Session is not valid, session is not active paid try.",
        "FA": "پرداخت ناموفق"
    },
    "-52": {
        "EN": "Oops!!, please contact our support team",
        "FA": "خطای غیر منتظره‌ای رخ داده است. پذیرنده مشکل خود را به امور مشتریان زرین‌پال ارجاع دهد."
    },
    "-53": {
        "EN": "Session is not this merchant_id session",
        "FA": "پرداخت متعلق به این مرچنت کد نیست."
    },
    "-54": {
        "EN": "Invalid authority.",
        "FA": "اتوریتی نامعتبر است."
    },
    "-55": {
        "EN": "manual payment request not found.",
        "FA": "تراکنش مورد نظر یافت نشد"
    },
    "-60": {
        "EN": "Session can not be reversed with bank.",
        "FA": "امکان ریورس کردن تراکنش با بانک وجود ندارد"
    },
    "-61": {
        "EN": "Session is not in success status.",
        "FA": "تراکنش موفق نیست یا قبلا ریورس شده است"
    },
    "-62": {
        "EN": "Terminal ip limit most be active.",
        "FA": "آی پی درگاه ست نشده است"
    },
    "-63": {
        "EN": "Maximum time for reverse this session is expired.",
        "FA": "حداکثر زمان (۳۰ دقیقه) برای ریورس کردن این تراکنش منقضی شده است"
    },
    "101": {
        "EN": "Verified",
        "FA": "تراکنش وریفای شده است."
    }
}

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
