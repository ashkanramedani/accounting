# from faker import Faker
import json
import re
from typing import List, Dict, Tuple, Any
from uuid import UUID

from sqlalchemy import text, asc, desc, or_, String, Integer, Float, Boolean
from sqlalchemy.orm import Session, Query

import db.models as dbm
import schemas as sch
from lib import logger

# key format
#   lower().replace("_form", "").replace("_", "")
# Value format]
#   dbm.<Table_name>
Tables = {
    "user": dbm.User_form,
    "student": dbm.User_form,
    "employee": dbm.User_form,
    "course": dbm.Course_form,
    "subcourse": dbm.Sub_Course_form,
    "session": dbm.Session_form,
    "leaverequest": dbm.Leave_Request_form,
    "businesstrip": dbm.Business_Trip_form,
    "remoterequest": dbm.Remote_Request_form,
    "paymentmethod": dbm.Payment_Method_form,
    "fingerprintscanner": dbm.Fingerprint_Scanner_form,
    "fingerprintscannerbackup": dbm.Fingerprint_Scanner_backup_form,
    "teachertardyreport": dbm.Teacher_Tardy_report_form,
    "teachersreport": dbm.Teachers_Report_form,
    # "survey": dbm.Survey_form,
    # "question": dbm.Question_form,
    # "response": dbm.Response_form,
    "role": dbm.Role_form,
    "salarypolicy": dbm.Salary_Policy_form,
    "employeesalary": dbm.Employee_Salary_form,
    "tag": dbm.Tag_form,
    "category": dbm.Category_form,
    "language": dbm.Language_form,
    "coursetype": dbm.Course_Type_form,
    # "status": dbm.Status_form,
    "subrequest": dbm.Sub_Request_form,
    "sessioncancellation": dbm.Session_Cancellation_form,
    # "reassigninstructor": dbm.Reassign_Instructor_form
}


def Add_tags_category(db: Session, course, course_pk_id: UUID, tags: List[sch.Update_Relation], categories: List[sch.Update_Relation]):
    Errors = []
    all_tags = [TAG.tag_pk_id for TAG in db.query(dbm.Tag_form).filter(dbm.Tag_form.status != "deleted").all()]
    all_categories = [CTG.category_pk_id for CTG in db.query(dbm.Category_form).filter(dbm.Category_form.status != "deleted").all()]
    for tag in tags:
        if existing_tag := tag.old_id:
            tag_OBJ = db.query(dbm.CourseTag).filter_by(course_fk_id=course_pk_id, tag_fk_id=existing_tag).filter(dbm.CourseTag.status != "deleted")
            if not tag_OBJ.first():
                Errors.append(f'Course does not have this tag {existing_tag}')
            else:
                tag_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_tag := tag.new_id:
            if new_tag not in all_tags:
                Errors.append(f'this tag does not exist {new_tag}')
            else:
                course.tags.append(db.query(dbm.Tag_form).filter_by(tag_pk_id=new_tag).filter(dbm.Tag_form.status != "deleted").first())

    for category in categories:
        if existing_category := category.old_id:
            category_OBJ = db.query(dbm.CourseCategory).filter_by(course_fk_id=course_pk_id, category_fk_id=existing_category).filter(dbm.CourseCategory.status != "deleted")
            if not category_OBJ.first():
                Errors.append(f'Course does not have this category {existing_category}')
            else:
                category_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_category := category.new_id:
            if new_category not in all_categories:
                Errors.append(f'this category does not exist {new_category}')
            else:
                course.categories.append(db.query(dbm.Category_form).filter_by(category_pk_id=new_category).filter(dbm.Category_form.status != "deleted").first())
    db.commit()
    return Errors


def Add_role(db, roles: List[sch.Update_Relation | Dict], UserOBJ, UserID):
    Errors = []
    role_ID: List[UUID] = [ID.role_pk_id for ID in db.query(dbm.Role_form).filter(dbm.Role_form.status != "deleted").all()]
    Roles = []
    for role in roles:
        if not isinstance(role, dict):
            Roles.append(role.__dict__)
        else:
            Roles.append(role)

    for r_id in Roles:
        if existing_role := r_id["old_id"]:
            role_obj = db.query(dbm.UserRole).filter_by(role_fk_id=existing_role, user_fk_id=UserID).filter(dbm.UserRole.status != "deleted")
            if not role_obj.first():
                Errors.append(f'Employee does not have this role {existing_role}')
            else:
                role_obj.update({"deleted": True}, synchronize_session=False)
        if new_role := r_id["new_id"]:
            if new_role not in role_ID:
                Errors.append(f'this role does not exist {new_role}')
            else:
                UserOBJ.roles.append(db.query(dbm.Role_form).filter_by(role_pk_id=new_role).filter(dbm.Role_form.status != "deleted").first())
    db.add(UserOBJ)
    db.commit()
    db.refresh(UserOBJ)
    return Errors


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.User_form).filter_by(user_pk_id=FK_field).filter(dbm.User_form.status != "deleted").first():
            return False
    return True


def course_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.Course_form).filter_by(course_pk_id=FK_field).filter(dbm.Course_form.status != "deleted").first():
        return False
    return True


def record_order_by(db: Session, table, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None, query: Query = None, **filter_kwargs) -> tuple[int, str] | tuple[int, list[Any]]:
    try:
        query = db.query(table).filter(table.status != "deleted").filter_by(**filter_kwargs) if not query else query

        # Search functionality
        # if SearchKey is not None:
        #     search_conditions = []
        #     for column in table.__table__.columns:
        #         column_type = column.type
        #         if isinstance(column_type, (String, Integer, Float)):
        #             search_conditions.append(column.ilike(f'%{SearchKey}%'))
        #         elif isinstance(column_type, Boolean):
        #             if SearchKey.lower() in ["true", "1"]:
        #                 search_conditions.append(column.is_(True))
        #             elif SearchKey.lower() in ["false", "0"]:
        #                 search_conditions.append(column.is_(False))
        #     query = query.filter(or_(*search_conditions))


        # Sort functionality
        if SortKey:
            if SortKey not in table.__table__.columns.keys():
                return Return_Exception(db, ValueError(f"Invalid key: {SortKey}"))

        TargetColumn = getattr(table, SortKey) if SortKey else table.create_date
        if order == "asc":
            query = query.order_by(TargetColumn)
        else:
            query = query.order_by(desc(TargetColumn))

        # Pagination
        if page > 0:
            query = query.offset((page - 1) * limit).limit(limit)

        return 200, query.all()

    except Exception as e:
        return Return_Exception(db, e)

def count(db, field: str):
    table = Tables.get(field.lower().replace("_form", "").replace("_", ""), None)
    if not table:
        return 404, f"{field} Not Found"
    return 200, db.query(table).filter(table.status != "deleted").count()


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


def Extract_Unique_keyPair(error_message) -> str | Dict:
    error_message = str(error_message)
    match = re.search(r'Key \((.*?)\)=\((.*?)\)', error_message)
    if match:
        return ', '.join([f'{k} -> {v}' for k, v in zip(match.group(1).split(', '), match.group(2).split(', '))]).replace('"', '')
    else:
        return error_message


def Return_Exception(db: Session, Error: Exception):
    db.rollback()
    if "duplicate key" in str(Error):
        logger.warning(f'{Error.__class__.__name__}: Record Already Exist: {Extract_Unique_keyPair(Error.args)}', depth=2)
        return 409, "Already Exist"
    logger.error(f'{Error.__class__.__name__}: {Error.__repr__()}', depth=2)
    return 500, f'{Error.__class__.__name__}: {Error.__repr__()}'


def Return_Test_Exception(Error: Exception):
    logger.error(Error, depth=2)
    if "UniqueViolation" in str(Error):
        return 409, "Already Exist"
    logger.error(Error)
    return 500, f'{Error.__class__.__name__}: {Error.__repr__()}'


def Primary_key(Obj):
    try:
        data = Obj if isinstance(Obj, Dict) else Obj.__dict__
        return next((val for key, val in data.items() if "_pk_" in key), None)
    except Exception as Error:
        return f'{Error.__class__.__name__}: {Error.__repr__()}'
