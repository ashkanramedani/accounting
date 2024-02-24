from sqlalchemy.orm import Session
from datetime import datetime
import sqlalchemy.sql.expression as sse
import logging
import schemas as sch
import db.models as dbm
from sqlalchemy import desc, asc
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def get_libraries_by_library_type(db: Session, library_type: str, limit: int):
    data = db.query(dbm.Libraries).filter(sse.and_(dbm.Libraries.library_type == library_type, dbm.Libraries.deleted == False, dbm.Libraries.visible == True)).order_by(dbm.Libraries.library_pk_id).limit(limit).all()
    if data is None:
        return False
    return data
# def update_libraries(db: Session, _id: int, update_obj: Libraries):
#     return 

# # delete
# def delete_libraries(db: Session, _id: int):
#     return 

# # insert
# def put_product(db: Session, new_obj: Libraries):
#     return  

# # select
# def get_libraries(db: Session, topic: str, limit: int):    
#     return db.query(Libraries).filter(sse.and_(Libraries.type == topic, Libraries.deleted == False)).order_by(Libraries.id).limit(limit).all()


# def get_product(db: Session, topic: str, uid:int):    
#     return db.query(Libraries).filter(sse.and_(Libraries.type == topic, Libraries.deleted == False, Libraries.id == uid)).first()