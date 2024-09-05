from sqlalchemy.orm import Session

import schemas as sch
import models as dbm
from ..Extra import *


# Student
def get_student(db: Session, student_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=student_id, is_employee=False).filter(dbm.User_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_student(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.User_form, page, limit, order, SortKey, is_employee=False)
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


def delete_student(db: Session, student_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=student_id).filter(dbm.User_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
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
