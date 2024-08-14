import re
from uuid import UUID
from typing import Dict, List
from sqlalchemy.orm import Session

from lib import logger
from db import models as dbm


def Extract_Unique_keyPair(error_message) -> str | Dict:
    error_message = str(error_message)
    match = re.search(r'Key \((.*?)\)=\((.*?)\)', error_message)
    if match:
        return ', '.join([f'{k} -> {v}' for k, v in zip(match.group(1).split(', '), match.group(2).split(', '))]).replace('"', '')
    else:
        return error_message


def Exception_handler(db, Error, Cluster: str = "Admin_Setup") -> None:
    db.rollback()
    if "duplicate key" in Error.__repr__() or "UniqueViolation" in Error.__repr__():
        logger.warning(f'[ {Cluster} / 409 ]{Error.__class__.__name__}: Record Already Exist: {Extract_Unique_keyPair(Error.args)}', depth=2)
        return
    logger.error(f'[ {Cluster} / 500 ]{Error.__class__.__name__}: {Error.__repr__()}', depth=2)


ADMIN: Dict = {"user_pk_id": "00000000-0000-4b94-8e27-44833c2b940f", "status": "approved", "fingerprint_scanner_user_id": None, "name": "Admin", "last_name": "Admin", "email": "Admin@Admin.com"}

DEFAULT_USER: List[Dict] = [
    {"user_pk_id": "00000001-0000-4b94-8e27-44833c2b940f", "status": "approved", "fingerprint_scanner_user_id": 1000, "name": "Test", "last_name": "Teacher", "email": "Test@Teacher.com"},
    {"user_pk_id": "00000002-0000-4b94-8e27-44833c2b940f", "status": "approved", "fingerprint_scanner_user_id": 1001, "name": "Test", "last_name": "Employee", "email": "Test@Employee.com"},
    {"user_pk_id": "00000003-0000-4b94-8e27-44833c2b940f", "status": "approved", "fingerprint_scanner_user_id": 1003, "name": "Test", "last_name": "Teacher2", "email": "Test@Teacher2.com"}
]

DEFAULT_ROLE: List[Dict] = [
    {"role_pk_id": "00000000-0001-4b94-8e27-44833c2b940f", "status": "approved", "name": "Administrator", "cluster": "Administrator"},
    {"role_pk_id": "00000001-0001-4b94-8e27-44833c2b940f", "status": "approved", "name": "Teacher", "cluster": "Teachers"},
    {"role_pk_id": "00000002-0001-4b94-8e27-44833c2b940f", "status": "approved", "name": "Student", "cluster": "Students"},
    {"role_pk_id": "00000003-0001-4b94-8e27-44833c2b940f", "status": "approved", "name": "Unknown", "cluster": "Users"}
]

USER_ROLE: List[Dict] = [
    {"user_fk_id": "00000000-0000-4b94-8e27-44833c2b940f", "status": "approved", "role_fk_id": "00000000-0001-4b94-8e27-44833c2b940f"},
    {"user_fk_id": "00000001-0000-4b94-8e27-44833c2b940f", "status": "approved", "role_fk_id": "00000001-0001-4b94-8e27-44833c2b940f"},
    {"user_fk_id": "00000002-0000-4b94-8e27-44833c2b940f", "status": "approved", "role_fk_id": "00000003-0001-4b94-8e27-44833c2b940f"}
]

DEFAULT_STATUS: List[Dict] = [
    {"status_pk_id": "00000000-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "submitted"},
    {"status_pk_id": "00000001-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "approved"},
    {"status_pk_id": "00000002-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "rejected"},
    {"status_pk_id": "00000003-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "pending"},
    {"status_pk_id": "00000004-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "cancelled"},
    {"status_pk_id": "00000005-0002-4b94-8e27-44833c2b940f", "status": "approved", "status_cluster": "form", "status_name": "deleted"},
]

DEFAULT_LANGUAGE: List[Dict] = [
    {"language_pk_id": "00000000-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "English"},
    {"language_pk_id": "00000001-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Spanish"},
    {"language_pk_id": "00000002-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Italian"},
    {"language_pk_id": "00000003-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "French"},
    {"language_pk_id": "00000004-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "German"},
    {"language_pk_id": "00000005-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Chinese"},
    {"language_pk_id": "00000006-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Japanese"},
    {"language_pk_id": "00000007-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Korean"},
    {"language_pk_id": "00000008-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Portuguese"},
    {"language_pk_id": "00000009-0003-4b94-8e27-44833c2b940f", "status": "approved", "language_name": "Russian"}
]

DEFAULT_COURSE_TYPE: List[Dict] = [
    {"course_type_pk_id": "00000000-0004-4b94-8e27-44833c2b940f", "status": "approved", "course_type_name": "online"},
    {"course_type_pk_id": "00000001-0004-4b94-8e27-44833c2b940f", "status": "approved", "course_type_name": "OnSite"},
    {"course_type_pk_id": "00000002-0004-4b94-8e27-44833c2b940f", "status": "approved", "course_type_name": "hybrid"}
]


def Create_Admin(db: Session) -> UUID:
    try:
        Admin_OBJ = db.query(dbm.User_form).filter_by(name="Admin", last_name="Admin").first()
        if not Admin_OBJ:
            Admin_OBJ = dbm.User_form(**ADMIN)  # type: ignore[call-arg]
            db.add(Admin_OBJ)
            db.commit()
            db.refresh(Admin_OBJ)
        return Admin_OBJ.user_pk_id
    except Exception as e:
        Exception_handler(db, e, "Create_Admin")


def Default_user(db: Session, ADIMN_ID: UUID):
    try:
        ExistingUsers = [str(user.user_pk_id) for user in db.query(dbm.User_form).filter(dbm.User_form.user_pk_id.in_([User["user_pk_id"] for User in DEFAULT_USER])).all()]
        New_Users = []
        for User in DEFAULT_USER:
            if User["user_pk_id"] not in ExistingUsers:
                New_Users.append(dbm.User_form(created_fk_by=ADIMN_ID, **User))  # type: ignore[call-arg]
        db.add_all(New_Users)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_user")


def Default_Role(db: Session, ADIMN_ID: UUID):
    try:
        Existing = [str(role.role_pk_id) for role in db.query(dbm.Role_form).filter(dbm.Role_form.role_pk_id.in_([r["role_pk_id"] for r in DEFAULT_ROLE])).all()]
        New_Roles = []

        for Role in DEFAULT_ROLE:
            if Role["role_pk_id"] not in Existing:
                New_Roles.append(dbm.Role_form(created_fk_by=ADIMN_ID, **Role))  # type: ignore[call-arg]
        db.add_all(New_Roles)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_role")


def Assign_Roles(db: Session):
    try:
        for record in USER_ROLE:
            User = db.query(dbm.User_form).filter_by(user_pk_id=record["user_fk_id"]).first()
            if Role := db.query(dbm.Role_form).filter_by(role_pk_id=record["role_fk_id"]).filter(dbm.Role_form.status != "deleted").first():
                User.roles.append(Role)
    except Exception as Error:
        Exception_handler(db, Error, "Assign_Roles")


def Default_Language(db: Session, ADIMN_ID: UUID):
    try:
        Existing = [str(record.language_pk_id) for record in db.query(dbm.Language_form).filter(dbm.Language_form.language_pk_id.in_([l["language_pk_id"] for l in DEFAULT_LANGUAGE])).all()]
        New_Languages = []

        for Language in DEFAULT_LANGUAGE:
            if Language["language_pk_id"] not in Existing:
                New_Languages.append(dbm.Language_form(created_fk_by=ADIMN_ID, **Language))  # type: ignore[call-arg]
        db.add_all(New_Languages)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_language")


def Default_Course_type(db: Session, ADIMN_ID: UUID):
    try:
        Existing = [str(record.course_type_pk_id) for record in db.query(dbm.Course_Type_form).filter(dbm.Course_Type_form.course_type_pk_id.in_([c["course_type_pk_id"] for c in DEFAULT_COURSE_TYPE])).all()]
        New_Course_Type = []

        for course_type in DEFAULT_COURSE_TYPE:
            if course_type["course_type_pk_id"] not in Existing:
                New_Course_Type.append(dbm.Course_Type_form(created_fk_by=ADIMN_ID, **course_type))  # type: ignore[call-arg]
        db.add_all(New_Course_Type)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_new_course_type")


def SetUp(db: Session):
    logger.info('Admin Setup Started')
    ADMIN_ID = Create_Admin(db)
    Default_user(db, ADMIN_ID)
    Default_Role(db, ADMIN_ID)
    Assign_Roles(db)
    Default_Language(db, ADMIN_ID)
    Default_Course_type(db, ADMIN_ID)
    logger.info('Admin Setup Finished')

"""
Create_Admin:85 - [ Create_Admin / 500 ]InvalidRequestError: InvalidRequestError('Entity namespace for "user" has no property "last_name"')
Default_user:98 - [ Default_user / 500 ]KeyError: KeyError('ID')
Default_Role:112 - [ Default_role / 500 ]IntegrityError: IntegrityError('(psycopg2.errors.NotNullViolation) null value in column "created_fk_by" of relation "role" violates not-null constraint\nDETAIL:  Failing row contains (5, t, f, t, t, 2024-07-25 07:11:15.628665+00, null, null, null, approved, , {}, 00000000-0001-4b94-8e27-44833c2b940f, null, Administrator, Administrator).\n')
Assign_Roles:122 - [ Assign_Roles / 500 ]InvalidRequestError: InvalidRequestError('Entity namespace for "user" has no property "user_fk_id"')
Default_Language:136 - [ Default_language / 500 ]IntegrityError: IntegrityError('(psycopg2.errors.NotNullViolation) null value in column "created_fk_by" of relation "language" violates not-null constraint\nDETAIL:  Failing row contains (5, t, f, t, t, 2024-07-25 07:11:15.840421+00, null, null, null, approved, , {}, 00000000-0003-4b94-8e27-44833c2b940f, English, null).\n')
Default_Course_type:150 - [ Default_new_course_type / 500 ]KeyError: KeyError('language_pk_id')
"""
