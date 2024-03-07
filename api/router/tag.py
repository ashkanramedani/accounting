from lib import log
logger = log()
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

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

from db import db_tag

router = APIRouter(prefix='/api/v1/tag', tags=['Tag'])



# @router.put("", response_model=sch.Tag, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def put_tag(tag: sch.TagCreate, db= Depends(get_db)):
#     tag_existed = db_tag.get_tag_by_name(db, tag.tag_name)
#     if tag_existed:
#         raise HTTPException(status_code=400, detail="این تگ وجود دارد")
#     return db_tag.create_tag(db=db, new=tag)

# @router.delete("", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def delete_tag_with_id(id, db=Depends(get_db)):
#     tag_existed = db_tag.get_tag_by_id(db, id)
#     if tag_existed is None:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 1")     
#     job = db_tag.delete_tag(db=db, id=id)
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام حذف خطایی رخ داده است.")    
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 2") 
#     elif job == 1:
#         return {"detail": "حذف با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام حذف خطایی رخ داده است.")

# @router.post("/disable", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def disable_visible_tag_with_id(id, db=Depends(get_db)):
#     tag_existed = db_tag.get_tag_by_id(db, id)
#     if tag_existed is None:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 1")    
#     tag_existed.visible = False
#     job = db_tag.update_tag(db=db, id=id, new=tag_existed)    
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام بروز رسانی خطایی رخ داده است.")    
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 2") 
#     elif job == 1:
#         return {"detail": "بروز رسانی با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام بروز رسانی خطایی رخ داده است.")

# @router.post("/enable", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
# def enable_visible_tag_with_id(id, db=Depends(get_db)):
#     tag_existed = db_tag.get_tag_by_id(db, id)
#     if tag_existed is None:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 1")
#     tag_existed.visible = True
#     job = db_tag.update_tag(db=db, id=id, new=tag_existed)
#     if job == -1:
#         raise HTTPException(status_code=501, detail="در انجام بروز رسانی خطایی رخ داده است.")
#     elif job == 0:
#         raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 2")
#     elif job == 1:
#         return {"detail": "بروز رسانی با موفقیت انجام شد"}
#     else:
#         raise HTTPException(status_code=502, detail="در انجام بروز رسانی خطایی رخ داده است.")

@router.get("/all", response_model=List[sch.Tag], dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_all_tag(db= Depends(get_db)):
    data = db_tag.get_all_tages(db)
    if not data:
        raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")            
    return data

@router.get("/{tag_id}", response_model=sch.Tag, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_tag_by_id(tag_id: str, db= Depends(get_db)):
    data = db_tag.get_tag_by_id(db, id=tag_id)
    if not data:
        raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 4")        
    return data

@router.get("", response_model=sch.Tag, dependencies=[Depends(RateLimiter(times=10, seconds=5))])
def get_tag_by_name(tag_name: str, db= Depends(get_db)):
    data = db_tag.get_tag_by_name(db, name=tag_name)
    if not data:
        raise HTTPException(status_code=404, detail="این تگ یافت نشد - کد 5")        
    return data
