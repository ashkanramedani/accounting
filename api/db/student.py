from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


# Student
def get_student(db: Session, student_id):
    try:
        return 200, db.query(dbm.Student_form).filter_by(student_pk_id=student_id,deleted=False).first()
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def get_all_student(db: Session):
    try:
        return 200, db.query(dbm.Student_form).filter_by(deleted=False).all()
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_student(db: Session, Form: sch.post_student_schema):
    try:
        OBJ = dbm.Student_form()

        OBJ.name = Form.name
        OBJ.last_name = Form.last_name
        OBJ.level = Form.level
        OBJ.age = Form.age

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Student Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def delete_student(db: Session, student_id):
    try:
        record = db.query(dbm.Student_form).filter_by(student_pk_id=student_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_student(db: Session, Form: sch.update_student_schema):
    try:
        record = db.query(dbm.Student_form).filter(dbm.Student_form.student_pk_id == Form.student_pk_id).first()
        if not record:
            return 404, "Record Not Found"
        record.student_name = Form.student_name
        record.student_last_name = Form.student_last_name
        record.student_level = Form.student_level
        record.student_age = Form.student_age
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()