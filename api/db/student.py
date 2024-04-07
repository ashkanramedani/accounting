from lib import logger


from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# Student
def get_student(db: Session, student_id):
    try:
        return 200, db.query(dbm.Student_form).filter_by(student_pk_id=student_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_student(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Student_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_student(db: Session, Form: sch.post_student_schema):
    try:
        OBJ = dbm.Student_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Student Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_student(db: Session, student_id):
    try:
        record = db.query(dbm.Student_form).filter_by(student_pk_id=student_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Student Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_student(db: Session, Form: sch.update_student_schema):
    try:
        record = db.query(dbm.Student_form).filter(dbm.Student_form.student_pk_id == Form.student_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
