from lib import logger

import schemas as sch
import db.models as dbm
import sqlalchemy.sql.expression as sse
from datetime import datetime, timedelta
from uuid import UUID
from typing import Optional, List, Dict, Any, Union, Annotated
from fastapi import APIRouter, Query, Body, Path, Depends, Response, HTTPException, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db.database import get_db
# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
from fastapi_limiter.depends import RateLimiter
from lib.hash import Hash
from lib.functions import Massenger, Tools

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

from db import db_category

router = APIRouter(prefix='/api/v1/category', tags=['Category'])

# @router.put("", response_model=sch.Category, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def put_category(category: sch.CategoryCreate, db= Depends(get_db)):
#     category_existed = db_category.get_category_by_name(db, category.category_name)
#     if category_existed:
#         raise HTTPException(status_code=400, detail="این دسته بندی وجود دارد")
#     return db_category.create_category(db=db, new=category)

# @router.delete("", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def delete_category_with_id(id, db=Depends(get_db)):
#     category_existed = db_category.get_category_by_id(db, id)
#     if category_existed is None:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 1")     
#     job = db_category.delete_category(db=db, id=id)
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام حذف خطایی رخ داده است.")    
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 2") 
#     elif job == 1:
#         return {"detail": "حذف با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام حذف خطایی رخ داده است.")

# @router.post("/disable", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def disable_visible_category_with_id(id, db=Depends(get_db)):
#     category_existed = db_category.get_category_by_id(db, id)
#     if category_existed is None:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 1")    
#     category_existed.visible = False
#     job = db_category.update_category(db=db, id=id, new=category_existed)    
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام بروز رسانی خطایی رخ داده است.")    
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 2") 
#     elif job == 1:
#         return {"detail": "بروز رسانی با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام بروز رسانی خطایی رخ داده است.")

# @router.post("/enable", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def enable_visible_category_with_id(id, db=Depends(get_db)):
#     category_existed = db_category.get_category_by_id(db, id)
#     if category_existed is None:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 1")
#     category_existed.visible = True
#     job = db_category.update_category(db=db, id=id, new=category_existed)
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام بروز رسانی خطایی رخ داده است.")
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 2")
#     elif job == 1:
#         return {"detail": "بروز رسانی با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام بروز رسانی خطایی رخ داده است.")

@router.get("/all", response_model=List[sch.Category], dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_all_category(db= Depends(get_db)):
    data = db_category.get_all_categoryes(db)
    if not data:
        raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")     
    return data

@router.get("/{category_id}", response_model=sch.Category, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_category_by_id(category_id: str, db= Depends(get_db)):
    data = db_category.get_category_by_id(db, id=category_id)
    if not data:
        raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 4")        
    return data

@router.get("", response_model=sch.Category, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_category_by_name(category_name: str, db= Depends(get_db)):
    data = db_category.get_category_by_name(db, name=category_name)
    if not data:
        raise HTTPException(status_code=404, detail="این دسته بندی یافت نشد - کد 5")        
    return data


