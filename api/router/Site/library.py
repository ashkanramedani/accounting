from typing import Optional, List, Any
from uuid import UUID

from docutils.nodes import topic
from fastapi import APIRouter, Depends, status, HTTPException

import db as dbf
import schemas as sch
from models import get_db

# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

router = APIRouter(prefix='/api/v1/library', tags=['Libraries'])


@router.post("/add", status_code=status.HTTP_200_OK)
def add_library(Form: sch.post_library, db=Depends(get_db)):
    status_code, result = dbf.post_library(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# read topics
@router.get('/get_library_topic', response_model=List[dict], status_code=status.HTTP_200_OK)
def get_library_topic() -> List:
    topics = [
        {"topic_name": "magazine", "label_name": "مجلات"},
        {"topic_name": "story", "label_name": "داستانی"},
        {"topic_name": "educational", "label_name": "آموزشی"}
    ]
    return topics


@router.get('/{topic}/read', status_code=status.HTTP_200_OK)
def get_all_library_with_limit(topic: str, page_number: Optional[int] = 0, limit: Optional[int] = 1000, db=Depends(get_db)) -> Any:
    status_code, result = dbf.read_all_library_for_admin_panel(db, topic, page_number, limit)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get('/{topic}/{pid}')
def get_library_with_pid(topic: str, pid: str, db=Depends(get_db)):
    status_code, result = dbf.get_library_with_pid(db, pid)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# delete libraries
@router.delete('/delete/{pid}', status_code=status.HTTP_200_OK)
def delete_library(pid: UUID, db=Depends(get_db)):
    status_code, result = dbf.delete_posts(db, pid)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete('/group-delete', status_code=status.HTTP_200_OK)
def delete_group_library(list_post: List[UUID], db=Depends(get_db)):
    return {str(ID): dbf.delete_libraries(db, topic) for ID in list_post}
