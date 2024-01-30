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
            if data:
                return data.__dict__
            return f"employee leave form Not Fount with ID: {employee_id}"
        data = db.query(dbm.Employees_signup_form).all()
        if data:
            return [record.__dict__ for record in data]
        return f"Empty Table: {employee_id}"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def post_employee(db: Session, Form: sch.Employee_schema):
    try:
        OBJ = dbm.Employees_signup_form(
                name=Form.name,
                last_name=Form.last_name,
                job_title=Form.job_title
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def delete_employee(db: Session, employee_id: int):
    try:
        if not db.query(dbm.Employees_signup_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first():
            return f"employee Does Not Exist with ID: {employee_id}"
        db.query(dbm.Leave_request_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).delete()
        db.commit()

    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def update_leave_form(db: Session, Form: sch.Employee_schema, employee_id: int):
    try:
        record = db.query(dbm.Employees_signup_form).filter(dbm.Employees_signup_form.employees_pk_id == employee_id).first()
        record.name = Form.name,
        record.last_name = Form.last_name,
        record.job_title = Form.job_title
        db.commit()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1
