from datetime import datetime

import sqlalchemy.sql.expression as sse
from sqlalchemy.orm import Session

from lib import log

logger = log()
import schemas as sch
import db.models as dbm


# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def get_tag_by_name(db: Session, name: str):
    data = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.tag_name == name, dbm.Tags.deleted == False)).first()
    if data is None:
        return False
    return data


def get_tag_by_id(db: Session, id: int):
    data = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.tag_pk_id == id, dbm.Tags.deleted == False)).first()
    if data is None:
        return False
    return data


def get_tages(db: Session, skip: int = 0, limit: int = 100):
    data = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.visible == True, dbm.Tags.deleted == False)).offset(skip).limit(limit).all()
    if data is None:
        return False
    return data


def get_all_tages(db: Session, page: int, limit: int):
    data = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.visible == True, dbm.Tags.deleted == False)).all()
    if data is None:
        return False
    return data


def create_tag(db: Session, new: sch.TagCreate):
    record = db.query(dbm.Tags).filter(dbm.Tags.tag_name == new.tag_name).first()
    if record is None or record.deleted == True or record.visible == False:
        tag_created = dbm.Tag(
                tag_name=new.tag_name,
                user_creator_tag_fk_id=new.user_creator_tag_fk_id
        )
        db.add(tag_created)
        db.commit()
        db.refresh(tag_created)
    else:
        tag_created = record
    return tag_created


def update_tag(db: Session, id: int, new: sch.Tag):
    try:
        record = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.tag_pk_id == id, dbm.Tags.can_update == True, dbm.Tags.deleted == False)).first()
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


def delete_tag(db: Session, id: int):
    try:
        record = db.query(dbm.Tags).filter(sse.and_(dbm.Tags.tag_pk_id == id, dbm.Tags.can_deleted == True, dbm.Tags.deleted == False)).first()
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
