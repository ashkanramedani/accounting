from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


# Student
def get_student(db: Session, student_id):
    try:
        record = db.query(dbm.Student_form).filter_by(
                student_pk_id=student_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def get_all_student(db: Session):
    try:
        data = db.query(dbm.Student_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def post_student(db: Session, Form: sch.post_student_schema):
    try:
        OBJ = dbm.Student_form()

        OBJ.student_name = Form.student_name
        OBJ.student_last_name = Form.student_last_name
        OBJ.student_level = Form.student_level
        OBJ.student_age = Form.student_age

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Student Added"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def delete_student(db: Session, student_id):
    try:
        record = db.query(dbm.Student_form).filter_by(
                student_pk_id=student_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def update_student(db: Session, Form: sch.update_student_schema):
    try:
        record = db.query(dbm.Student_form).filter(dbm.Student_form.student_pk_id == Form.student_pk_id).first()
        if not record:
            return 404, "Not Found"
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
        return 500, e.args[0]

#
