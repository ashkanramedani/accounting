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

# 0 - غیر فعال
# 1 - تایید نشده
# 2 - تایید شده/ فعال

from db import db_post

router = APIRouter(prefix='/api/v1/post', tags=['Post'])

# read topics
@router.get('/get_post_topic', response_model=List[dict], status_code=status.HTTP_200_OK)
def get_post_topic() -> List:
    topics = [
        {
            "topic_name": "news", 
            "label_name": "اخبار"
        },
        {
            "topic_name": "blog", 
            "label_name": "بلاگ"
        },
        {
            "topic_name": "podcast", 
            "label_name": "پادکست"
        }
    ]
    return topics

# create posts
@router.post('', status_code=201)
def create_a_post(post:sch.PostCreate, db=Depends(get_db)) -> Any:
    data = None

    data = db_post.create_post(db, post)

    if data is None or data is False:
        raise HTTPException(status_code=500, detail="خطایی رخ داده است")

    return data

# update posts
@router.put('/{topic}', status_code=status.HTTP_200_OK)
def partial_modifications_all_post_in_topic(topic:str, post:sch.PostCreate, db=Depends(get_db)) -> Any:
    return {"detail": "در دست ساخت است"}

# update posts
@router.patch('/update/{pid}', status_code=status.HTTP_200_OK)
def partial_modifications_in_a_post(topic:str, post:sch.PostCreate, pid:str, db=Depends(get_db)) -> Any:
    return {"detail": "در دست ساخت است"} 

@router.patch('/group-partial-modifications-in-group-post', status_code=status.HTTP_200_OK)
def group_partial_modifications_in_group_post(list_post:List[sch.PostCreate], db=Depends(get_db)) -> Any:
    return {"detail": "در دست ساخت است"} 

@router.patch('/group-status-modifications-in-group-post', status_code=status.HTTP_200_OK)
def group_status_modifications_in_group_post(list_post:List[sch.PostStatus], db=Depends(get_db)) -> Any:
    return {"detail": "در دست ساخت است"} 

# delete posts
@router.delete('/delete/{pid}', status_code=status.HTTP_200_OK)
def delete_post(pid:int, db=Depends(get_db)) -> Any:
    res = db_post.delete_posts(db, topic, pid)
    if res == 1:
        return Response(status_code=200, content="داده با موفقیت حذف شد")

    elif res == 0:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    elif res == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

@router.delete('/group-delete', status_code=status.HTTP_200_OK)
def group_delete_post(list_post:List[sch.PostDelete], db=Depends(get_db)) -> Any:
    res = None
    for i in list_pid:
        if res is None:
            res = {}
        if i not in res:
            res[i] = db_post.delete_posts(db, topic, i)
    
    return res

# read post - get posts all posts with limit
@router.get('/{topic}/read', response_model=List[sch.Posts], status_code=status.HTTP_200_OK)
def get_all_posts_with_limit(topic:str, start_id:Optional[int]=0, page_number:Optional[int]=0, limit:Optional[int]=1000, db=Depends(get_db)) -> Any:
    data = db_post.read_all_posts_for_admin_panel(db, topic, start_id, page_number, limit)

    if data == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

    if not data or data is None or data == [] or data is False:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    return data

@router.get('/{topic}/{pid}', response_model=sch.Posts)
def get_post_with_pid(topic:str, pid:str, db=Depends(get_db)):
    data = db_post.get_post_with_pid(db, pid)

    if data == -1:
        return Response(status_code=500, content="خطایی رخ داده است")

    if not data or data is None or data == [] or data is False:
        return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

    return data



# get posts with search posts with limit
# @router.get('/{topic}/search', response_model=List[sch.Posts], status_code=status.HTTP_200_OK)
# def get_all_posts_with_limit_with_search(q:Optional[str], topic:str, limit:Optional[int]=1000, db=Depends(get_db)):
#     res = []
#     data = db_post.get_all_posts_with_limit(db, topic, limit)
#     for i in data:
#         if i.post_title is not None and str(q).lower() in str(i.post_title).lower():
#             res.append(i) 
#         elif i.post_Summary is not None and str(q).lower() in str(i.post_Summary).lower():
#             res.append(i) 
#         elif i.post_discribtion is not None and str(q).lower() in str(i.post_discribtion).lower():
#             res.append(i) 
#         elif i.post_content is not None and str(q).lower() in str(i.post_content).lower():
#             res.append(i)    
#     for i in res:
#         viwe = db_post.get_viwe(db, i.post_pk_id)
#         i.viwe = viwe
#     return res

# # get posts all posts with page and limit
# @router.get('/{topic}/', response_model=List[sch.Posts])
# def get_all_posts_with_page_and_limit(topic:str, page:Optional[int]=0, limit:Optional[int]=9, db=Depends(get_db)) -> Any:
#     data = db_post.get_all_posts_with_page_and_limit(db, topic, limit, page)
#     for i in data:
#         viwe = db_post.get_viwe(db, i.post_pk_id)
#         i.viwe = viwe
#     return data

# # get posts one post
# @router.get('/{topic}', response_model=sch.Post)
# def get_one_post(topic:str, id:int, db=Depends(get_db)) -> Any:
#     data = db_post.get_post(db, topic, id)
#     viwe = db_post.get_viwe(db, id)
#     data.viwe = viwe
#     return data

# # get posts one post
# @router.put('/{topic}/viwe')
# def get_one_post(topic:str, data:sch.PostViwesCreate, db=Depends(get_db)) -> Any:
#     resviwe = db_post.put_viwe(db, data)
#     return True



# @router.put('/{topic}/update/{pid}', status_code=status.HTTP_200_OK)
# def update_post(topic:str, pid:int, update:sch.PostUpdateData, db=Depends(get_db)) -> Any:
#     res = db_posts.update_posts(db, topic, pid, update)   
#     if res == 1:
#         return Response(status_code=200, content="اطلاعات با موفقیت بروز رسانی شد")

#     elif res == 0:
#         return Response(status_code=404, content="هیچ داده‌ای یافت نشد")

#     elif res == -1:
#         return Response(status_code=500, content="خطایی رخ داده است")
