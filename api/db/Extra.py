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
    "role": dbm.Roles_form,
    "remote_request": dbm.Remote_Request_form,
    "question": dbm.Questions_form,
    "response": dbm.Response_form,
    "business_trip": dbm.Business_Trip_form,
    "course_cancellation": dbm.course_Cancellation_form,
    "employee": dbm.Employees_form,
    "tardy_request": dbm.Teacher_tardy_reports_form,
    "student": dbm.Student_form,
    "teacher_replacement": dbm.Teacher_Replacement_form,
    "course": dbm.course_form,
    "fingerprint_scanner": dbm.Fingerprint_scanner_form,
    "payment_method": dbm.Payment_method_form,
    "leave_forms": dbm.Leave_request_form
}

# table = {
# "course": dbm.course_form,
# "sub_course": dbm.sub_course_form,
# "employee": dbm.Employees_form,
# "student": dbm.Student_form,
# "question": dbm.Questions_form,
# "survey": dbm.Survey_form,
# "course_type": dbm.Course_Type_form,
# "session": dbm.Session_form,
# "leave_request": dbm.Leave_request_form,
# "business_trip": dbm.Business_Trip_form,
# "remote_request": dbm.Remote_Request_form,
# "payment_method": dbm.Payment_method_form,
# "FingerPrintScanner": dbm.Fingerprint_scanner_form,
# "teacher_tardy_reports": dbm.Teacher_tardy_reports_form,
# "course_cancellation": dbm.course_Cancellation_form,
# "teacher_replacement": dbm.Remote_Request_form,
# # "teachers_report": dbm.,
# # "response": dbm.,
# # "role": dbm.,
# # "SalaryPolicy": dbm.,
# # "salary": dbm.,
# # "tag": dbm.,
# # "category": dbm.,
# # "language": dbm.,
# }

__all__ = [
    "employee_exist",
    "course_exist",
    'record_order_by',
    'count',
    'safe_run']




def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'{e.__class__.__name__}: {e.args}')
        return func(*args, **kwargs)

    return wrapper


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True


def course_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.course_form).filter_by(course_pk_id=FK_field, deleted=False).first():
        return False
    return True


def record_order_by(db: Session, table, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    if order == "desc":
        return db.query(table).filter_by(deleted=False).order_by(table.create_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return db.query(table).filter_by(deleted=False).order_by(table.create_date.asc()).offset((page - 1) * limit).limit(limit).all()


def count(db, field: str):
    field = field.lower().replace(" ", "_")
    if field not in Tables:
        return 404, "field Not Found"
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



if __name__ == '__main__':
    pass
