# from faker import Faker
from typing import List, Dict, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger

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


def Add_role(db, roles: List[sch.Update_Relation | Dict], UserOBJ, UserID):
    Errors = []
    role_ID: List[UUID] = [ID.role_pk_id for ID in db.query(dbm.Role_form).filter_by(deleted=False).all()]
    Roles = []
    for role in roles:
        if not isinstance(role, dict):
            Roles.append(role.__dict__)
        else:
            Roles.append(role)

    for r_id in Roles:
        if existing_role := r_id["old_id"]:
            role_obj = db.query(dbm.UserRole).filter_by(role_fk_id=existing_role, user_fk_id=UserID, deleted=False)
            if not role_obj.first():
                Errors.append(f'Employee does not have this role {existing_role}')
            else:
                role_obj.update({"deleted": True}, synchronize_session=False)
        if new_role := r_id["new_id"]:
            if new_role not in role_ID:
                Errors.append(f'this role does not exist {new_role}')
            else:
                UserOBJ.roles.append(db.query(dbm.Role_form).filter_by(role_pk_id=new_role, deleted=False).first())
    db.commit()
    return Errors


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




def Exist(db: Session, Form: Dict) -> Tuple[bool, str]:
    for key, val in Form.items():
        if "fk" in key or "pk" in key:
            table, params = prepare_param(key, val)
            if not table:
                return False, f"{params} Not Found"
            if not db.query(table).filter_by(**params).first():
                return False, f'{key} Not Found in {table}'
    return True, "Done"


def Return_Exception(db: Session, Error: Exception):
    logger.error(Error, depth=2)
    db.rollback()
    if "UniqueViolation" in str(Error):
        return 409, "Already Exist"
    return 500, f'{Error.__class__.__name__}: {Error.args}'
