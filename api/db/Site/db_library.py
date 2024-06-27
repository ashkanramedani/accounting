from datetime import datetime

import sqlalchemy.sql.expression as sse
from sqlalchemy.orm import Session

import db.models as dbm
from lib import logger


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def get_libraries_by_library_type(db: Session, library_type: str, limit: int):
    data = db.query(dbm.Libraries).filter(sse.and_(dbm.Libraries.library_type == library_type, dbm.Libraries.deleted == False, dbm.Libraries.visible == True)).order_by(dbm.Libraries.library_pk_id).limit(limit).all()
    if data is None:
        return False
    return data


def read_all_library_for_admin_panel(db: Session, topic: str, start_id: int, page_number: int, limit: int):
    try:
        data = db.query(dbm.Libraries).filter(sse.and_(dbm.Libraries.library_type == topic, dbm.Libraries.deleted == False, dbm.Libraries.library_pk_id >= start_id)).order_by(dbm.Libraries.library_pk_id.desc()).limit(limit).all()
        if data is None:
            return False
        return data
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


def get_library_with_pid(db: Session, pid: str):
    try:
        data = db.query(dbm.Libraries).filter(sse.and_(dbm.Libraries.library_pk_id == pid, dbm.Libraries.deleted == False)).first()
        if data is None:
            return False
        return data
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


# delete
def delete_libraries(db: Session, topic: str, pid: int):
    try:
        record = db.query(dbm.Libraries).filter(sse.and_(dbm.Libraries.deleted == False, dbm.Libraries.library_pk_id == pid, dbm.Libraries.can_deleted == True)).first()
        if record is not None:
            record.deleted = True
            record.delete_date = datetime.utcnow()
            db.commit()
            return 1
        else:
            return 0
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1

# # insert
# def put_product(db: Session, new_obj: Libraries):
#     return  

# # select
# def get_libraries(db: Session, topic: str, limit: int):    
#     return db.query(Libraries).filter(sse.and_(Libraries.type == topic, Libraries.deleted == False)).order_by(Libraries.id).limit(limit).all()


# def get_product(db: Session, topic: str, uid:int):    
#     return db.query(Libraries).filter(sse.and_(Libraries.type == topic, Libraries.deleted == False, Libraries.id == uid)).first()
