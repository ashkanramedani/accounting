from typing import List, Dict
from uuid import UUID
from lib import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from ..Extra import *

def get_employee(db: Session, employee_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=employee_id, deleted=False, is_employee=True).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_employee(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.User_form, page, limit, order, is_employee=True)
    except Exception as e:
        return Return_Exception(db, e)


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        data = Form.dict()
        roles: List[sch.Update_Relation | str] | str = data.pop("roles") if "roles" in data else None

        if data["name"] == "Admin":
            return 400, "illegal Name Admin"

        OBJ = dbm.User_form(**data, is_employee=True)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if not roles or isinstance(roles, str):
            return 200, f'Employee Added. ID: {OBJ.user_pk_id}'

        Error = Add_role(db, roles, OBJ, OBJ.user_pk_id)
        if Error:
            return 200, "Employee Added But there was an error in roles: " + " | ".join(Error)
        return 200, f'Employee Added. ID: {OBJ.user_pk_id}'
    except Exception as e:
        return Return_Exception(db, e)


def delete_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=employee_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        if record.name == "Admin":
            return 400, "Admin Cont be deleted"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=Form.user_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        if data["name"] == "Admin":
            return 400, "illegal Name Admin"

        roles: List[sch.Update_Relation | str] | str = data.pop("roles") if "roles" in data else None
        record.update(data, synchronize_session=False)
        db.commit()

        if not roles:
            return 200, "Record Updated"

        Error = Add_role(db, roles, record.first(), Form.user_pk_id)
        if Error:
            return 200, "Record Updated But there was an error in roles: " + " | ".join(Error)
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)