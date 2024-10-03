import re
from time import sleep
from uuid import UUID
from typing import Dict, List, Tuple

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from lib import logger
import models.tables as dbm
from models.Triggers import archive_deleted_record


def Extract_Unique_keyPair(error_message) -> str | Dict:
    error_message = str(error_message)
    match = re.search(r'Key \((.*?)\)=\((.*?)\)', error_message)
    if match:
        return ', '.join([f'{k} -> {v}' for k, v in zip(match.group(1).split(', '), match.group(2).split(', '))]).replace('"', '')
    else:
        return error_message


CODES = {
    "user": "0",
    "role": "1",
    "status": "2",
    "language": "3",
    "course_type": "4"
}

def Exception_handler(db, Error, Cluster: str = "Admin_Setup") -> None:
    db.rollback()
    if "duplicate key" in Error.__repr__() or "UniqueViolation" in Error.__repr__():
        logger.warning(f'[ {Cluster} / 409 ]{Error.__class__.__name__}: Record Already Exist: {Extract_Unique_keyPair(Error.args)}', depth=2)
        return
    logger.error(f'[ {Cluster} / 500 ]{Error.__class__.__name__}: {Error.__repr__()}', depth=2)

def Unique_ID(num: int, code: str) -> str:
    return f"{str(num).zfill(8)}-{CODES.get(code, 0).zfill(4)}-4b94-8e27-44833c2b940f"



# Name, LastName, FID
USER: List[Tuple] = [
    ("Admin", "Admin", None),
    ("Test", "Teacher", 1000),
    ("Test", "Employee", 1001),
    ("Test", "Teacher2", 1003)
]
# Cluster, Name
ROLE: List[Tuple] = [
    ("Administrator", "Administrator"),
    ("Teachers", "Teacher"),
    ("Students", "Student"),
    ("Users", "Unknown")
]
# Cluster, Name
STATUS: List[Tuple] = [
    ("form", "submitted"),
    ("form", "approved"),
    ("form", "rejected"),
    ("form", "pending"),
    ("form", "cancelled"),
    ("form", "deleted"),
    ("form", "in_progress"),
    ("form", "closed"),
    ("form", "created")]
# user, role
USER_ROLE_MAP: List[Tuple] = [
    ("00000000-0000-4b94-8e27-44833c2b940f", "00000000-0001-4b94-8e27-44833c2b940f"),
    ("00000001-0000-4b94-8e27-44833c2b940f", "00000001-0001-4b94-8e27-44833c2b940f"),
    ("00000002-0000-4b94-8e27-44833c2b940f", "00000003-0001-4b94-8e27-44833c2b940f")
]
LANGUAGE: List[str] = [
    "English",
    "Spanish",
    "Italian",
    "French",
    "German",
    "Chinese",
    "Japanese",
    "Korean",
    "Portuguese",
    "Russian"]
COURSE_TYPE: List[str] = [
    "online",
    "OnSite",
    "hybrid"]


def Default_user(db: Session):
    DEFAULT_USER: List[Dict] = [
        {"user_pk_id": Unique_ID(i, "user"), "status": "approved", "fingerprint_scanner_user_id": FID, "name": N, "last_name": L, "email": f"{N}@{L}.com"}
        for i, (N, L, FID) in enumerate(USER)]

    Admin_id = DEFAULT_USER[0]["user_pk_id"]

    try:
        ExistingUsers = [str(user.user_pk_id) for user in db.query(dbm.User_form).filter(dbm.User_form.user_pk_id.in_([User["user_pk_id"] for User in DEFAULT_USER])).all()]
        New_Users = []
        for User in DEFAULT_USER:
            if User["user_pk_id"] not in ExistingUsers:
                New_Users.append(dbm.User_form(created_fk_by=Admin_id, **User))  # type: ignore[call-arg]
        db.add_all(New_Users)
        db.commit()
        return Admin_id
    except Exception as Error:
        Exception_handler(db, Error, "Default_user")


def Default_Role(db: Session, Admin_id: UUID):
    try:
        DEFAULT_ROLE: List[Dict] = [
            {"role_pk_id": Unique_ID(i, "role"), "status": "approved", "name": N, "cluster": C}
            for i, (C, N) in enumerate(ROLE)]

        Existing = [str(role.role_pk_id) for role in db.query(dbm.Role_form).filter(dbm.Role_form.role_pk_id.in_([r["role_pk_id"] for r in DEFAULT_ROLE])).all()]
        New_Roles = []

        for Role in DEFAULT_ROLE:
            if Role["role_pk_id"] not in Existing:
                New_Roles.append(dbm.Role_form(created_fk_by=Admin_id, **Role))  # type: ignore[call-arg]
        db.add_all(New_Roles)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_role")


def Assign_Roles(db: Session):
    try:
        USER_ROLE: List[Dict] = [
            {"user_fk_id": U, "status": "approved", "role_fk_id": R}
            for U, R in USER_ROLE_MAP
        ]
        for record in USER_ROLE:
            User = db.query(dbm.User_form).filter_by(user_pk_id=record["user_fk_id"]).first()
            if Role := db.query(dbm.Role_form).filter_by(role_pk_id=record["role_fk_id"]).filter(dbm.Role_form.status != "deleted").first():
                User.roles.append(Role)
    except Exception as Error:
        Exception_handler(db, Error, "Assign_Roles")


def Default_Status(db: Session, Admin_id: UUID):
    try:
        DEFAULT_STATUS: List[Dict] = [
            {"status_pk_id": Unique_ID(i, "status"), "status": "approved", "status_cluster": C, "status_name": S}
            for i, (C, S) in enumerate(STATUS)]
        Existing = [f'{record.status_cluster}/{record.status_name}' for record in db.query(dbm.Status_form).filter(dbm.Status_form.status_pk_id.in_([s["status_pk_id"] for s in DEFAULT_STATUS])).all()]
        New_Status = []

        for Status in DEFAULT_STATUS:
            if f'{Status["status_cluster"]}/{Status["status_name"]}' not in Existing:
                New_Status.append(dbm.Status_form(created_fk_by=Admin_id, **Status))  # type: ignore[call-arg]
        db.add_all(New_Status)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_Status")


def Default_Language(db: Session, Admin_id: UUID):
    try:
        DEFAULT_LANGUAGE: List[Dict] = [
            {"language_pk_id": Unique_ID(i, "language"), "status": "approved", "language_name": LN}
            for i, LN in enumerate(LANGUAGE)]
        Existing = [str(record.language_pk_id) for record in db.query(dbm.Language_form).filter(dbm.Language_form.language_pk_id.in_([l["language_pk_id"] for l in DEFAULT_LANGUAGE])).all()]
        New_Languages = []

        for Language in DEFAULT_LANGUAGE:
            if Language["language_pk_id"] not in Existing:
                New_Languages.append(dbm.Language_form(created_fk_by=Admin_id, **Language))  # type: ignore[call-arg]
        db.add_all(New_Languages)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_language")


def Default_Course_type(db: Session, Admin_id: UUID):
    try:
        DEFAULT_COURSE_TYPE: List[Dict] = [
            {"course_type_pk_id": Unique_ID(i, "course_type"), "status": "approved", "course_type_name": CT}
            for i, CT in enumerate(COURSE_TYPE)]

        Existing = [str(record.course_type_pk_id) for record in db.query(dbm.Course_Type_form).filter(dbm.Course_Type_form.course_type_pk_id.in_([c["course_type_pk_id"] for c in DEFAULT_COURSE_TYPE])).all()]
        New_Course_Type = []

        for course_type in DEFAULT_COURSE_TYPE:
            if course_type["course_type_pk_id"] not in Existing:
                New_Course_Type.append(dbm.Course_Type_form(created_fk_by=Admin_id, **course_type))  # type: ignore[call-arg]
        db.add_all(New_Course_Type)
        db.commit()
    except Exception as Error:
        Exception_handler(db, Error, "Default_new_course_type")


def SetUp_table(engine):
    try:
        logger.info("Connecting To Database")
        TRY = 0

        while True and TRY < 10:
            try:
                dbm.Base.metadata.create_all(bind=engine)
                TRY = 0
                break
            except OperationalError as OE:
                TRY += 1
                logger.warning(f"[ Could Not Create Engine ]: {OE.__repr__()}")
                sleep(10)

        if TRY != 0:
            logger.error(f"Could Not Create Engine after {TRY} times")
            return False
        logger.info("Setting Up Listeners")
        for cls in dbm.Base.__subclasses__():
            if "_form" in cls.__name__:
                event.listen(cls, 'before_delete', archive_deleted_record)
        logger.info("Database Setup finished")
        return True
    except Exception as e:
        logger.error(f"Database Setup failed: {e}")
        return False


def SetUp(db: Session):
    logger.info('Admin Setup Started')
    ADMIN_ID = Default_user(db)
    Default_Role(db, ADMIN_ID)
    Assign_Roles(db)
    Default_Status(db, ADMIN_ID)
    Default_Language(db, ADMIN_ID)
    Default_Course_type(db, ADMIN_ID)
    logger.info('Admin Setup Finished')
