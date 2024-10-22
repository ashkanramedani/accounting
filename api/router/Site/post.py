from typing import Optional, List, Any
from uuid import UUID

from docutils.nodes import topic
from fastapi import APIRouter, Depends, HTTPException, status

import db as dbf
import schemas as sch
from models import get_db

# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
# 0 - غیر فعال
# 1 - تایید نشده
# 2 - تایید شده/ فعال

router = APIRouter(prefix='/api/v1/post', tags=['Post'])


# read topics
@router.get('/get_post_topic', response_model=List[dict], status_code=status.HTTP_200_OK)
def get_post_topic() -> List:
    topics = [
        {"topic_name": "news", "label_name": "اخبار"},
        {"topic_name": "blog", "label_name": "بلاگ"},
        {"topic_name": "podcast", "label_name": "پادکست"}
    ]
    return topics


# create posts
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_a_post(Form: sch.create_post, db=Depends(get_db)):
    status_code, result = dbf.create_post(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# delete posts
@router.delete('/delete/{pid}', status_code=status.HTTP_200_OK)
def delete_post(pid: UUID, db=Depends(get_db)) -> Any:
    status_code, result = dbf.delete_posts(db, topic, pid)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete('/group-delete', status_code=status.HTTP_200_OK)
def group_delete_post(posts: List[UUID], db=Depends(get_db)):
    return {str(ID): dbf.delete_posts(db, topic, ID) for ID in posts}


@router.get('/{topic}/read', response_model=List[sch.Posts], status_code=status.HTTP_200_OK)
def get_all_posts_with_limit(topic: str, page_number: Optional[int] = 0, limit: Optional[int] = 1000, db=Depends(get_db)):
    status_code, result = dbf.read_all_posts_for_admin_panel(db, topic, page_number, limit)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get('/{topic}/{pid}', response_model=sch.Posts)
def get_post_with_pid(pid: UUID, db=Depends(get_db)):
    status_code, result = dbf.get_post_with_pid(db, pid)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
