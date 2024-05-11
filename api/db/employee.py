from typing import List
from uuid import UUID
from lib import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


def Add_role(db, roles: List[sch.Update_Relation], EMP_obj, Employee_id):
    Errors = []
    role_ID: List[UUID] = [ID.role_pk_id for ID in db.query(dbm.Role_form).filter_by(deleted=False).all()]

    for r_id in roles:
        if existing_role := r_id.old_id:
            role_obj = db.query(dbm.UserRole).filter_by(role_fk_id=existing_role, user_fk_id=Employee_id, deleted=False)
            if not role_obj.first():
                Errors.append(f'Employee does not have this role {existing_role}')
            else:
                role_obj.update({"deleted": True}, synchronize_session=False)
        if new_role := r_id.new_id:
            if new_role not in role_ID:
                Errors.append(f'this role does not exist {new_role}')
            else:
                EMP_obj.roles.append(db.query(dbm.Role_form).filter_by(role_pk_id=new_role, deleted=False).first())
    db.commit()
    return Errors
def get_employee(db: Session, employee_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=employee_id, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_employee(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.User_form, page, limit, order)
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
            return 200, "EEmployee Added But there was an error in roles: " + " | ".join(Error)
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
