from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


def get_class(db: Session, class_id):
    try:
        record = db.query(dbm.Class_form).filter_by(
                classs_pk_id=class_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def get_all_class(db: Session):
    try:
        data = db.query(dbm.Class_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_class(db: Session, Form: sch.post_class_schema):
    try:
        OBJ = dbm.Class_form()

        OBJ.starting_time = Form.starting_time
        OBJ.duration = Form.duration
        OBJ.class_date = Form.class_date

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "class Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def delete_class(db: Session, class_id):
    try:
        record = db.query(dbm.Class_form).filter_by(
                class_id=class_id,
                deleted=False
        ).first()
        if not record or record.deleted:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_class(db: Session, Form: sch.update_class_schema):
    try:
        record = db.query(dbm.Class_form).filter_by(
                classs_pk_id=Form.class_pk_id,
                deleted=True
        ).first()
        if not record:
            return 404, "Not Found"

        record.starting_time = Form.starting_time
        record.duration = Form.duration
        record.class_date = Form.class_date
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
