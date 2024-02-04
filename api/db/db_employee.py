from uuid import UUID
from typing import List
from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

__all__ = [
    "get_employee",
    "get_all_employee",
    "post_employee",
    "delete_employee",
    "update_employee",
    "get_student",
    "post_student",
    "delete_student",
    "update_student",

]

def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True

def get_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(
                employees_pk_id=employee_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def get_all_employee(db: Session):
    try:
        data = db.query(dbm.Employees_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        OBJ = dbm.Employees_form(
                name=Form.name,
                last_name=Form.last_name,
                job_title=Form.job_title
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Employee Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def delete_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(
                employee_id=employee_id,
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


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.Employees_form).filter(dbm.Employees_form.employees_pk_id == Form.employees_pk_id).first()
        if not record or record.deleted:
            return 404, "Not Found"
        record.name = Form.name,
        record.last_name = Form.last_name,
        record.job_title = Form.job_title
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()


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
        return 500, e.__repr__()


def get_all_student(db: Session):
    try:
        data = db.query(dbm.Student_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_student(db: Session, Form: sch.post_student_schema):
    try:
        OBJ = dbm.Student_form(
                student_name=Form.student_name,
                student_last_name=Form.student_last_name,
                student_level=Form.student_level,
                student_age=Form.student_age
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Student Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


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
        return 500, e.__repr__()


def update_student(db: Session, Form: sch.update_student_schema):
    try:
        record = db.query(dbm.Student_form).filter(dbm.Student_form.student_pk_id == Form.student_pk_id).first()
        if not record:
            return 404, "Not Found"
        record.student_name = Form.student_name
        record.student_last_name = Form.student_last_name
        record.student_level = Form.student_level
        record.student_age = Form.student_age

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()

#
