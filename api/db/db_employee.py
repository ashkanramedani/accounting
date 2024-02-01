from sqlalchemy.orm import Session
from datetime import datetime
import sqlalchemy.sql.expression as sse
import logging
import api.schemas as sch
import api.db.models as dbm
from sqlalchemy import desc, asc
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from typing import Optional, List, Dict, Any


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def get_employee(db: Session, employee_id: int | None = None):
    try:
        if isinstance(employee_id, int):
            data = db.query(dbm.Employees_signup_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        else:
            data = db.query(dbm.Employees_signup_form).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_employee(db: Session, Form: sch.Employee_post_schema):
    try:
        OBJ = dbm.Employees_signup_form(
                name=Form.name,
                last_name=Form.last_name,
                job_title=Form.job_title
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_employee(db: Session, employee_id: int):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        if not record or record.deleted is True:
            return 404, f"employee Does Not Exist with ID: {employee_id}"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_leave_form(db: Session, Form: sch.Employee_post_schema, employee_id: int):
    try:
        record = db.query(dbm.Employees_signup_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        record.name = Form.name,
        record.last_name = Form.last_name,
        record.job_title = Form.job_title
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# Student

# class Student_form(BaseTable):
#     __tablename__ = "student"
#     student_pk_id = create_Unique_ID()
#     student_name = Column(String, nullable=False)
#     student_last_name = Column(String, index=True)
#     student__level = Column(String, index=True)
#     student_age = Column(Integer)
#

def get_student(db: Session, Form: sch.get_student):
    try:
        if isinstance(Form.student_id, UUID):
            data = db.query(dbm.Student_form).filter(dbm.Student_form.student_pk_id == Form.student_id).first()
        else:
            data = db.query(dbm.Student_form).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_employee(db: Session, Form: sch.Employee_post_schema):
    try:
        OBJ = dbm.Employees_signup_form(
                name=Form.name,
                last_name=Form.last_name,
                job_title=Form.job_title
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_employee(db: Session, employee_id: int):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        if not record or record.deleted is True:
            return 404, f"employee Does Not Exist with ID: {employee_id}"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_leave_form(db: Session, Form: sch.Employee_post_schema, employee_id: int):
    try:
        record = db.query(dbm.Employees_signup_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        record.name = Form.name,
        record.last_name = Form.last_name,
        record.job_title = Form.job_title
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
