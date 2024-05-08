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
from db.models import get_db
# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
from fastapi_limiter.depends import RateLimiter
from lib.hash import Hash
from lib.functions import Massenger, Tools

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

from db import db_user#, db_post, db_role, db_gender, db_branch, db_educationalInstitution

router = APIRouter(prefix='/api/v1/user', tags=['User'])


@router.get("/employees")
def get_employees_users(role: Optional[str]=None, skip: Optional[int]=0, limit: Optional[int]=1000, db=Depends(get_db)):
    if role is None:
        users = db_user.get_users_withfilter_employes(db, skip, limit)
        # logging.error(users)
    # else:
    #     pass

    return users

# @router.post("/set_role", response_model=sch.UserWithMoreInfo)
# def put_set_role(user_id: int, role_id: int, hash_key:str="3c456a61-4adb-4ac2-ad0c-c0adbea05fac", db=Depends(get_db)):
    
#     objeducationalInstitution = db_educationalInstitution.get_educationalInstitutions_by_educational_institution_hash(db, hash_key)
#     if objeducationalInstitution is None:
#         raise HTTPException(status_code=404, detail="چنین موسسه ای وجود ندارد")       
    
#     objuser = db.query(dbm.Users).filter(sse.and_(dbm.Users.user_pk_id == user_id, dbm.Users.deleted == False)).first()
#     if objuser is None:
#         raise HTTPException(status_code=404, detail="چنین کاربری وجود ندارد")       
  
#     objrole = db.query(dbm.Roles).filter(sse.and_(dbm.Roles.role_pk_id == role_id, dbm.Roles.deleted == False)).first()
#     if objrole is None:
#         raise HTTPException(status_code=404, detail="چنین نقشی وجود ندارد")       
    
#     data = db_user.put_role_for_user(db, user=objuser, role=objrole, educational_institution=objeducationalInstitution)

#     if not data:
#         raise HTTPException(status_code=500, detail="در ایجاد نقش جدید برای کاربر مشکلی وجود دارد")
#     return data

# @router.get("/me", response_model=sch.UserWithMe)
# def get_user(db= Depends(get_db), token:str=Depends(oauth2_scheme)):
#     data = get_current_user(token, db)
#     # data = db_user.get_user_by_id(db, id=current_user.user_pk_id)
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data

# @router.get('/check/{key}')
# def check_is_exsisted_user(key: str, val: str, db=Depends(get_db)):
#     data = None
#     action = 'register'
#     auth_type = None

#     if key == 'email':
#         action = 'login'
#         auth_type = 'password'
#         data = db_user.get_user_by_email(db, val)

#     elif key == 'mobile_number':
#         action = 'login'
#         auth_type = 'otp'
#         data = db_user.get_user_by_mobile_number(db, val)

#     if not data:
#         return { "action": 'register', "exsisted": False, "auth_type": None }    

#     else:
#         return { "action": action, "exsisted": True, "auth_type": auth_type }

# @router.get("/{user_id}", response_model=sch.UserWithMoreInfo)
# def get_user(user_id: int, db=Depends(get_db)) -> Any:
#     data = db_user.get_user_by_id(db, id=user_id)
#     for i in data.posts_user_speaker: 
#         viwe = db_post.get_viwe(db, i.post_pk_id)
#         i.viwe = viwe
#     for i in data.posts_user_writer: 
#         viwe = db_post.get_viwe(db, i.post_pk_id)
#         i.viwe = viwe
#     for i in data.posts_user_actor: 
#         viwe = db_post.get_viwe(db, i.post_pk_id)
#         i.viwe = viwe
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data

# @router.put('')
# def create_user(user:sch.UserCreate, hash_key:str="3c456a61-4adb-4ac2-ad0c-c0adbea05fac", db=Depends(get_db), token:str=Depends(oauth2_scheme)): #, token:str=Depends(oauth2_scheme)

#     educationalInstitution = db_educationalInstitution.get_educationalInstitutions_by_educational_institution_hash(db, hash_key)
#     if educationalInstitution is None:
#         raise HTTPException(status_code=404, detail="چنین موسسه ای وجود ندارد")       
    
#     role = db.query(dbm.Roles).filter(sse.and_(dbm.Roles.role_name == user.role_name, dbm.Roles.deleted == False)).first()
#     if role is None:
#         raise HTTPException(status_code=404, detail="چنین نقشی وجود ندارد")       
    
#     branch = db.query(dbm.Branchs).filter(sse.and_(dbm.Branchs.branch_name == user.branch, dbm.Branchs.deleted == False)).first()
#     if branch is None:
#         raise HTTPException(status_code=404, detail="چنین شعبه‌ای وجود ندارد")       
    
#     gender = db.query(dbm.Genders).filter(sse.and_(dbm.Genders.gender_name == user.gender, dbm.Genders.deleted == False)).first()
#     if gender is None:
#         raise HTTPException(status_code=404, detail="چنین جنسیتی وجود ندارد")       

#     newUser = db_user.put_user(db, user, branch.branch_pk_id, gender.gender_pk_id, role, educationalInstitution)
#     if newUser is None:
#         raise HTTPException(status_code=500, detail="در ایجاد کاربر جدید مشکلی وجود دارد")
    
#     return newUser

# 205
# @router.delete('')
# def get_user(user_id: Optional[int]=None, db=Depends(get_db), token:str=Depends(oauth2_scheme)) -> Any:
#     data = db_user.delete_user(db, _id=user_id)
#     if data == 1:
#         return {'detail':'کاربر با موفقیت حذف شد'}
#     if data == 0:
#         return {'detail':'کاربر با این مشخصات یافت نشد'}
#     return {'detail':'خطایی رخ داده است'}

# @router.post("", response_model=List[sch.UserWithMoreInfo])
# def read_users(skip: int, limit: int, db= Depends(get_db)):
#     data = db_user.get_users(db, skip=skip, limit=limit)
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data


# @router.get("/all", response_model=List[sch.UserWithMoreInfo])
# def get_all_users(skip: int, limit: int, db= Depends(get_db), token:str=Depends(oauth2_scheme)):
#     data = db_user.get_users(db, skip=skip, limit=limit)
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data

# @router.get('/employes')
# def get_all_employes_users(skip: int, limit: int, db=Depends(get_db)):
#     data = db_user.get_users_withfilter_employes(db, skip=skip, limit=limit)
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data

# @router.get('/general')
# def get_all_not_employes_users(skip: int, limit: int, db=Depends(get_db), token:str=Depends(oauth2_scheme)):
#     data = db_user.get_users_withfilter_not_employes(db, skip=skip, limit=limit)
#     if not data:
#         raise HTTPException(status_code=404, detail="هیچ داده ای یافت نشد.")       
#     return data

# @router.get("/me/get_all_placement", response_model=List[Dict])
# def get_all_placement_me(db= Depends(get_db), token:str=Depends(oauth2_scheme)):
#     current_user = get_current_user(token, db)
#     # user = db_user.get_user_by_id(db, id=current_user.user_pk_id)
#     return [
#         {
#             "name": "english",
#             "label": "انگلیسی",
#             "placment": "C2",
#             "placment_data": {
#             "vocabulary": 6,
#             "reading": 8,
#             "speaking": 7,
#             "grammar": 7,
#             "writing": 7.5
#             }
#         },
#         {
#             "name": "italian",
#             "label": "ایتالیایی",
#             "placment": "C2",
#             "placment_data": {
#             "vocabulary": 6,
#             "reading": 8,
#             "speaking": 7,
#             "grammar": 7,
#             "writing": 7.5
#             }
#         }
#     ]

# @router.delete('/{user_id}')
# def delete_user(user_id:int, db=Depends(get_db), token:str=Depends(oauth2_scheme)):    
#     # res = db_user.(db, uid)
#     # if res == 1:
#     #     return Response(status_code=200, content="1")
#     # elif res == 0:
#     #     return Response(status_code=404, content="0")
#     # elif res == -1:
#     #     return Response(status_code=500,content="-1")
#     # else:
#     #     return Response(status_code=501, content="-2")
#     pass
