from lib.Date_Time import *

import json
from functools import wraps

# from faker import Faker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date
from typing import List, Dict, Tuple
from uuid import UUID
from random import choice as r_ch
import schemas as sch
import db.models as dbm
from lib import logger


import re

Tables = {
    "survey": dbm.Survey_form,
    "role": dbm.Role_form,
    "remote_request": dbm.Remote_Request_form,
    "question": dbm.Question_form,
    "response": dbm.Response_form,
    "business_trip": dbm.Business_Trip_form,
    "course_cancellation": dbm.Course_Cancellation_form,
    "employee": dbm.User_form,
    "tardy_request": dbm.Teacher_Tardy_report_form,
    "student": dbm.User_form,
    "teacher_replacement": dbm.Teacher_Replacement_form,
    "course": dbm.Course_form,
    "fingerprint_scanner": dbm.Fingerprint_Scanner_form,
    "payment_method": dbm.Payment_Method_form,
    "leave_forms": dbm.Leave_Request_form
}


__all__ = [
    "employee_exist",
    "course_exist",
    'record_order_by',
    'count',
    'safe_run',
    'log_on_status']




def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        return func(*args, **kwargs)

    return wrapper


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.User_form).filter_by(user_pk_id=FK_field, deleted=False).first():
            return False
    return True


def course_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.Course_form).filter_by(course_pk_id=FK_field, deleted=False).first():
        return False
    return True


def record_order_by(db: Session, table, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    if order == "desc":
        return db.query(table).filter_by(deleted=False).order_by(table.create_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return db.query(table).filter_by(deleted=False).order_by(table.create_date.asc()).offset((page - 1) * limit).limit(limit).all()


def count(db, field: str):
    field = field.lower().replace(" ", "_")
    if field not in Tables:
        return 400, "field Not Found"
    return 200, len(db.query(Tables[field]).filter_by(deleted=False).all())

def prepare_param(key, val):
    table = key.lower().replace("_fk_id", "").replace("_pk_id", "")
    if key in ["created", "session_main_teacher", "session_sub_teacher", "employee", "teacher", "employees"]:
        table = "employee"
    elif table not in Tables:
        return None, table
    return Tables[table], {"deleted": False, key.replace("_fk_id", "_pk_id"): val}

def Exist(db: Session, Form: Dict) -> Tuple[bool, str]:
    for key, val in Form.items():
        if "fk" in key or "pk" in key:
            table, params = prepare_param(key, val)
            if not table:
                return False, f"{params} Not Found"
            if not db.query(table).filter_by(**params).first():
                return False, f'{key} Not Found in {table}'
    return True, "Done"


import functools

def log_on_status(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs) -> Tuple[int, str]:
    status, message = func(*args, **kwargs)
    logger.on_status_code(status, message)
    return status, message
  return wrapper


if __name__ == '__main__':
    pass

"""
https://sand.admin.api.ieltsdaily.ir/count?field=Employee
"""