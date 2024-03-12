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

from db import db_library

router = APIRouter(prefix='/api/v1/library', tags=['Libraries'])

# # create libraries
# @router.put('')
# def create_libraries(db=Depends(get_db)):
#     pass

# get products
# @router.get("/{library_type}", response_model=List[sch.Library], dependencies=[Depends(RateLimiter(times=10, seconds=2))])
# def get_libraries_by_library_type(library_type: str, limit:Optional[int]=5, q:Optional[str]="", db=Depends(get_db)):
#     data = db_library.get_libraries_by_library_type(db, library_type=library_type, limit=limit)
#     if not data:
#         return False #raise HTTPException(status_code=404, detail="کتابی یافت نشد - کد ۱")     

#     if q is not None or q != "":
#         res = []
#         for i in data:
#             if str(q).lower() in str(i.library_name).lower():
#                 res.append(i)
#         return res 
#     return data


# @router.get('/{topic}')
# def get_libraries(topic: str="public", limit:Optional[int]=1000, db=Depends(get_db)):
#     data = db_libraries.get_libraries(db, topic, limit)
#     res = []
#     for i in data:
#         res.append(            
#             {
#                 "id": i.id,
#                 "name": i.name,
#                 "image": i.image,
#                 "type": i.type,
#                 "description": i.description,
#                 "summer": i.summer,
#                 "download_count": i.download_count,
#                 "priority": i.priority,
#                 "audio_file_link": i.audio_file_link,
#                 "audio_file_path": i.audio_file_path,
#                 "aparat_video_id": i.aparat_video_id,
#                 "aparat_video_code": i.aparat_video_code,
#                 "video_file_link":  i.video_file_link,
#                 "video_file_path": i.video_file_path,
#                 "data_file_link": i.data_file_link,
#                 "data_file_path": i.data_file_path,
#                 "create_date": i.create_date,
#                 "expire_date": i.expire_date
#             }
#         )
#     return res

# @router.get('/{topic}/{uid}')
# def get_libraries_info(uid: int, topic: Optional[str]="public", db=Depends(get_db)):
#     i = db_libraries.get_libraries(db, topic, uid)
#     res =   {
#         "id": i.id,
#         "name": i.name,
#         "image": i.image,
#         "type": i.type,
#         "description": i.description,
#         "summer": i.summer,
#         "download_count": i.download_count,
#         "priority": i.priority,
#         "audio_file_link": i.audio_file_link,
#         "audio_file_path": i.audio_file_path,
#         "aparat_video_id": i.aparat_video_id,
#         "aparat_video_code": i.aparat_video_code,
#         "video_file_link":  i.video_file_link,
#         "video_file_path": i.video_file_path,
#         "data_file_link": i.data_file_link,
#         "data_file_path": i.data_file_path,
#         "create_date": i.create_date,
#         "expire_date": i.expire_date
#     }
#     return res

# read topics
@router.get('/get_library_topic', response_model=List[dict], status_code=status.HTTP_200_OK)
def get_library_topic() -> List:
    topics = [
        {
            "topic_name": "magazine", 
            "label_name": "مجلات"
        },
        {
            "topic_name": "story", 
            "label_name": "داستانی"
        },
        {
            "topic_name": "educational", 
            "label_name": "آموزشی"
        }
    ]
    return topics

@router.get('/{topic}/read', response_model=List[sch.Library], status_code=status.HTTP_200_OK)
def get_all_library_with_limit(topic:str, start_id:Optional[int]=0, page_number:Optional[int]=0, limit:Optional[int]=1000, db=Depends(get_db)) -> Any:
    data = db_library.read_all_library_for_admin_panel(db, topic, start_id, page_number, limit)

    if data == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

    if not data or data is None or data == [] or data is False:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    return data

@router.get('/{topic}/{pid}', response_model=sch.Library)
def get_library_with_pid(topic:str, pid:str, db=Depends(get_db)):
    data = db_library.get_library_with_pid(db, pid)

    if data == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

    if not data or data is None or data == [] or data is False:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    return data

# create libraries
@router.post('', status_code=201)
def create_library(db=Depends(get_db)):
    pass

# update libraries
@router.patch('/update/{lid}')
def update_library(lid:str, db=Depends(get_db)):
    pass

@router.patch('/group-partial-modifications-in-group-library')
def group_partial_modifications_in_group_library(db=Depends(get_db)):
    pass

@router.patch('/group-status-modifications-in-group-library')
def group_status_modifications_in_group_library(db=Depends(get_db)):
    pass

# delete libraries
@router.delete('/delete/{lid}', status_code=status.HTTP_200_OK)
def delete_library(lid:str, db=Depends(get_db)):
    res = db_library.delete_posts(db, topic, pid)
    if res == 1:
        return Response(status_code=200, content="داده با موفقیت حذف شد")

    elif res == 0:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    elif res == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

@router.delete('/group-delete', status_code=status.HTTP_200_OK)
def delete_group_library(list_post:List[sch.LibraryDelete], db=Depends(get_db)) -> Any:
    res = None
    for i in list_pid:
        if res is None:
            res = {}
        if i not in res:
            res[i] = db_library.delete_libraries(db, topic, i)
    
    return res