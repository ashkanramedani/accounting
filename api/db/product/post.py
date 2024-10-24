from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import *

import models as dbm
import schemas as sch
from db import Return_Exception


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

# read
def read_all_posts_for_admin_panel(db: Session, topic: str, page_number: int, limit: int):
    try:
        return 200, db \
            .query(dbm.Posts_form) \
            .filter(dbm.Posts_form.post_type == topic) \
            .order_by(dbm.Posts_form.post_pk_id.desc()) \
            .limit(limit) \
            .all()

    except Exception as e:
        return Return_Exception(db, e)


def get_post_with_pid(db: Session, pid: UUID):
    try:
        return db.query(dbm.Posts_form).filter(dbm.Posts_form.post_pk_id == pid).first()
    except Exception as e:
        return Return_Exception(db, e)


# delete
def delete_posts(db: Session, pid: UUID, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Posts_form).filter(and_(dbm.Posts_form.deleted == False, dbm.Posts_form.post_pk_id == pid, dbm.Posts_form.can_deleted == True)).first()
        if not record:
            return 404, "record not found"

        record._Deleted_BY = deleted_by
        db.commit()
        return 200, "Success"
    except Exception as e:
        return Return_Exception(db, e)


# update
def update_posts(db: Session, pid: UUID, Form: sch.update_post_schema):
    try:
        record = db \
            .query(dbm.Posts_form) \
            .filter(dbm.Posts_form.post_pk_id == pid)

        if not record.first():
            return 404, "post not found"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Updated"
    except Exception as e:
        return Return_Exception(db, e)


# insert
def create_post(db: Session, Form: sch.create_post):
    try:
        data = Form.__dict__
        category = data.pop("category")
        tag = data.pop("tag")

        users_post_speaker = data.pop("users_post_speaker")
        users_post_writer = data.pop("users_post_writer")
        users_post_actor = data.pop("users_post_actor")

        data = dbm.Posts_form(**data)  # type: ignore[call_args]
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return Return_Exception(db, e)
