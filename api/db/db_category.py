from datetime import datetime

import sqlalchemy.sql.expression as sse
from sqlalchemy.orm import Session

from lib import log

logger = log()
import schemas as sch
import db.models as dbm


# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


def get_category_by_name(db: Session, name: str):
    data = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.category_name == name, dbm.Categories.deleted == False)).first()
    if data is None:
        return False
    return data


def get_category_by_id(db: Session, id: int):
    data = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.category_pk_id == id, dbm.Categories.deleted == False)).first()
    if data is None:
        return False
    return data


def get_categoryes(db: Session, skip: int = 0, limit: int = 100):
    data = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.visible == True, dbm.Categories.deleted == False)).offset(skip).limit(limit).all()
    if data is None:
        return False
    return data


def get_all_categoryes(db: Session):
    data = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.visible == True, dbm.Categories.deleted == False)).all()
    if data is None:
        return False
    return data


def create_category(db: Session, new: sch.CategoryCreate):
    record = db.query(dbm.Categories).filter(dbm.Categories.category_name == new.category_name).first()
    if record is None or record.deleted == True or record.visible == False:
        category_created = dbm.Categories(
                category_name=new.category_name,
                user_creator_category_fk_id=new.user_creator_category_fk_id
        )
        db.add(category_created)
        db.commit()
        db.refresh(category_created)
    else:
        category_created = record
    return category_created


def update_category(db: Session, id: int, new: sch.Category):
    try:
        record = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.category_pk_id == id, dbm.Categories.can_update == True, dbm.Categories.deleted == False)).first()
        if record is not None:
            if new.visible != record.visible:
                record.visible = new.visible

            record.update_date = datetime.utcnow()
            db.commit()
            return 1
        else:
            return 0
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


def delete_category(db: Session, id: int):
    try:
        record = db.query(dbm.Categories).filter(sse.and_(dbm.Categories.category_pk_id == id, dbm.Categories.can_deleted == True, dbm.Categories.deleted == False)).first()
        if record is not None:
            record.visible = False
            record.deleted = True

            record.delete_date = datetime.utcnow()
            record.update_date = datetime.utcnow()
            db.commit()
            return 1
        else:
            return 0
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1
