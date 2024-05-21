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


def Add_tags_category(db: Session, course, course_pk_id: UUID, tags: List[sch.Update_Relation], categories: List[sch.Update_Relation]):
    Errors = []
    all_tags = [id.tag_pk_id for id in db.query(dbm.Tag_form).filter_by(deleted=False).all()]
    all_categories = [id.category_pk_id for id in db.query(dbm.Category_form).filter_by(deleted=False).all()]
    for tag in tags:
        if existing_tag := tag.old_id:
            tag_OBJ = db.query(dbm.CourseTag).filter_by(course_fk_id=course_pk_id, tag_fk_id=existing_tag, deleted=False)
            if not tag_OBJ.first():
                Errors.append(f'Course does not have this tag {existing_tag}')
            else:
                tag_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_tag := tag.new_id:
            if new_tag not in all_tags:
                Errors.append(f'this tag does not exist {new_tag}')
            else:
                course.tags.append(db.query(dbm.Tag_form).filter_by(tag_pk_id=new_tag, deleted=False).first())

    for category in categories:
        if existing_category := category.old_id:
            category_OBJ = db.query(dbm.CourseCategory).filter_by(course_fk_id=course_pk_id, category_fk_id=existing_category, deleted=False)
            if not category_OBJ.first():
                Errors.append(f'Course does not have this category {existing_category}')
            else:
                category_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_category := category.new_id:
            if new_category not in all_categories:
                Errors.append(f'this category does not exist {new_category}')
            else:
                course.categories.append(db.query(dbm.Category_form).filter_by(category_pk_id=new_category, deleted=False).first())
    db.commit()
    return Errors



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


def Return_Exception(db: Session, Error: Exception):
    logger.error(Error, depth=2)
    db.rollback()
    if "UniqueViolation" in str(Error):
        return 409, "Already Exist"
    return 500, f'{Error.__class__.__name__}: {Error.args}'
