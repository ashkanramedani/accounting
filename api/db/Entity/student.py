from sqlalchemy.orm import Session

from db import models as dbm
import schemas as sch
from ..Extra import *


# Student
def get_student(db: Session, student_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=student_id, deleted=False, is_employee=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_student(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.User_form, page, limit, order, is_employee=False)
    except Exception as e:
        return Return_Exception(db, e)


def post_student(db: Session, Form: sch.post_student_schema):
    try:
        OBJ = dbm.User_form(**Form.dict(), is_employee=False)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Student Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_student(db: Session, student_id):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=student_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Student Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_student(db: Session, Form: sch.update_student_schema):
    try:
        record = db.query(dbm.User_form).filter(dbm.User_form.user_pk_id == Form.user_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
