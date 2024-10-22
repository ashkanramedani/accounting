from datetime import datetime
from typing import Tuple, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

import models as dbm
from db import Return_Exception
import schemas as sch


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


def post_library(db: Session, Form: sch.post_library):
    try:
        data = dbm.Posts_form(**Form.__dict__)  # type: ignore[call_args]
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return Return_Exception(db, e)


def get_libraries_by_library_type(db: Session, library_type: str, limit: int) -> Tuple[int, Any]:
    try:
        return 200, db \
            .query(dbm.Library_form) \
            .filter(dbm.Library_form.library_type == library_type) \
            .order_by(dbm.Library_form.library_pk_id) \
            .limit(limit) \
            .all()

    except Exception as e:
        return Return_Exception(db, e)


def read_all_library_for_admin_panel(db: Session, topic: str, page_number: int, limit: int) -> Tuple[int, Any]:
    try:
        return 200, db \
            .query(dbm.Library_form) \
            .filter(dbm.Library_form.library_type == topic) \
            .order_by(dbm.Library_form.library_pk_id.desc()) \
            .limit(limit) \
            .all()
    except Exception as e:
        return Return_Exception(db, e)


def get_library_with_pid(db: Session, pid: str) -> Tuple[int, Any]:
    try:
        return 200, db.query(dbm.Library_form).filter(dbm.Library_form.library_pk_id == pid).first()
    except Exception as e:
        return Return_Exception(db, e)


# delete
def delete_libraries(db: Session, pid: UUID, deleted_by: UUID = None) -> Tuple[int, Any]:
    try:
        record = db \
            .query(dbm.Library_form) \
            .filter(dbm.Library_form.library_pk_id == pid)

        if not record.first():
            return 404, "Record Not Found"
        record._Deleted_By = deleted_by
        record.delete()
        db.commit()

    except Exception as e:
        return Return_Exception(db, e)
