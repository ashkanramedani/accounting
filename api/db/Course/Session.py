from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger

from ..Extra import *
from lib.Date_Time import *
from datetime import timedelta, datetime


# ------ Session -------
def get_session(db: Session, session_id):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=session_id, deleted=False).first()
        if not session:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, session
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_session(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Session_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_session(db: Session, Form: sch.post_session_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.session_teacher_fk_id]):
            return 400, "Bad Request: employee not found"

        if not db.query(dbm.sub_course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id, deleted=False).first():
            return 400, "Bad Request: sub course not found"

        if not db.query(dbm.course_form).filter_by(course_pk_id=Form.course_fk_id, deleted=False).first():
            return 400, "Bad Request: course not found"

        OBJ = dbm.Session_form(**Form.__dict__)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "session Added"
    except Exception as e:
        db.rollback()
        logger.error(e)
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_session(db: Session, course_id):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=course_id, deleted=False).first()
        if not record:
            return 400, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        logger.error(e)
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_session(db: Session, Form: sch.update_session_schema):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_pk_id, deleted=False)
        if not record.first():
            return 400, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
