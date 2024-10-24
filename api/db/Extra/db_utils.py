# from faker import Faker
import re
from datetime import timedelta, timezone
from typing import List, Dict, Tuple, Any
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session, Query

import models as dbm
import schemas as sch
from lib import logger

IRAN_TIMEZONE = timezone(offset=timedelta(hours=3, minutes=30))

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
    "role": dbm.Role_form,
    "salarypolicy": dbm.Salary_Policy_form,
    "employeesalary": dbm.Employee_Salary_form,
    "tag": dbm.Tag_form,
    "category": dbm.Category_form,
    "language": dbm.Language_form,
    "coursetype": dbm.Course_Type_form,
    "subrequest": dbm.Sub_Request_form,
    "sessioncancellation": dbm.Session_Cancellation_form,
    "rewardcard": dbm.Reward_card_form,
    # "survey": dbm.Survey_form,
    # "question": dbm.Question_form,
    # "response": dbm.Response_form,
    # "status": dbm.Status_form,
    # "reassigninstructor": dbm.Reassign_Instructor_form
}


def Add_tags(db: Session, course, tags: List[sch.Update_Relation]):
    try:
        tag_ids = [tag.new_id for tag in tags] + [tag.old_id for tag in tags]

        all_tags = db.query(dbm.Tag_form).filter(dbm.Tag_form.status != "deleted", dbm.Tag_form.tag_pk_id.in_(tag_ids)).all()

        new_tag_ids, old_tag_ids = {tag.new_id for tag in tags}, {tag.old_id for tag in tags}

        current_tags = set(course.tags)

        for tag in all_tags:
            if tag.tag_pk_id in new_tag_ids and tag not in current_tags:
                course.tags.append(tag)
            elif tag.tag_pk_id in old_tag_ids and tag in current_tags:
                course.tags.remove(tag)
        return None
    except Exception as e:
        return f'{e.__class__.__name__}: {e.__repr__()}'


def Add_categories(db: Session, course, categories: List[sch.Update_Relation]) -> str:
    try:
        category_ids: List[UUID] = [category.new_id for category in categories] + [category.old_id for category in categories]

        all_categories: List[dbm.Category_form] = db.query(dbm.Category_form).filter(dbm.Category_form.status != "deleted", dbm.Category_form.category_pk_id.in_(category_ids)).all()

        new_category_ids, old_category_ids = {category.new_id for category in categories}, {category.old_id for category in categories}

        current_categories = set(course.categories)

        for category in all_categories:
            if category.category_pk_id in new_category_ids and category not in current_categories:
                course.categories.append(category)
            elif category.category_pk_id in old_category_ids and category in current_categories:
                course.categories.remove(category)
        return ""
    except Exception as e:
        return f'{e.__class__.__name__}: {e.__repr__()}'


def Add_role(db, roles: List[sch.Update_Relation | Dict], UserOBJ, UserID):
    Errors = []
    role_ID: List[UUID] = [ID.role_pk_id for ID in db.query(dbm.Role_form).filter(dbm.Role_form.status != "deleted").all()]

    Roles = [role.__dict__ if not isinstance(role, dict) else role for role in roles]

    for r_id in Roles:
        if existing_role := r_id["old_id"]:
            role_obj = db.query(dbm.UserRole).filter_by(role_fk_id=existing_role, user_fk_id=UserID, deleted=False)
            if not role_obj.first():
                Errors.append(f'Employee does not have this role {existing_role}')
            else:
                role_obj.delete()
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
    field = field.lower().replace("_form", "").replace("_", "")
    table = Tables.get(field, None)

    if not table:
        return 404, f"{field} Not Found"
    query: Query = db.query(table).filter(table.status != "deleted")
    if field == "student":
        query = query.filter_by(is_employee=False)
    elif field == "employee":
        query = query.filter_by(is_employee=True)

    return 200, query.count()


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


def Return_Exception(db: Session = None, Error: Exception = None):
    if db:
        db.rollback()

    ERR_MSG = Error.__repr__()
    if "duplicate key" in ERR_MSG or "UniqueViolation" in ERR_MSG:
        logger.warning(f'{Error.__class__.__name__}: Record Already Exist: {Extract_Unique_keyPair(Error.args)}', depth=2)
        return 409, "Already Exist"
    logger.error(f'{Error.__class__.__name__}: {ERR_MSG}', depth=2)
    return 500, f'{Error.__class__.__name__}: {ERR_MSG}'


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
