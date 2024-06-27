import uuid

from sqlalchemy.orm import Session

from db import models as dbm
from lib import logger

ADMIN = {
    "name": "Admin",
    "lastname": "Admin",
    "role": {"name": "Administrator", "cluster": "Administrator"}}

DEFAULT_ROLES = [
    {"name": "Manager", "cluster": "Manager"},
    {"name": "Unknown", "cluster": "Users"},
    {"name": "Student", "cluster": "Users"},
    {"name": "Support", "cluster": "Supports"},
    {"name": "Teacher", "cluster": "Teachers"}
]


DEFAULT_STATUS = {
    "form": ["submitted", "approved", "rejected", "pending", "cancelled"],
    "payment": []
}

DEFAULT_LANGUAGE = ["Not_Assigned", "English", "Spanish", "Italian", "French", "German", "Chinese", "Japanese", "Korean", "Portuguese", "Russian"]
DEFAULT_COURSE_TYPE = ["Not_Assigned", "Online", "Offline", "OnSite"]


def setUp_admin(db: Session):
    try:
        emp = db.query(dbm.User_form).filter_by(name=ADMIN["name"]).first()
        if not emp:
            UID = "308e2744-833c-4b94-8e27-44833c2b940f"
            admin_user = dbm.User_form(user_pk_id=UID, created_fk_by=UID, name=ADMIN["name"], last_name=ADMIN["lastname"], email="Admin@Admin.com", status=1)  # type: ignore[call-arg]
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            emp = admin_user

            admin_role = db.query(dbm.Role_form).filter_by(name=ADMIN["role"]["name"]).first()
            if not admin_role:
                admin_role = dbm.Role_form(created_fk_by=emp.user_pk_id, name=ADMIN["role"]["name"], cluster=ADMIN["role"]["cluster"], status=1)  # type: ignore[call-arg]
                db.add(admin_role)
                db.commit()

            emp.roles.append(admin_role)

        existing_role_names = [role.name for role in db.query(dbm.Role_form).filter(dbm.Role_form.name.in_([r["name"] for r in DEFAULT_ROLES])).all()]
        new_OBJ = []

        for role_data in DEFAULT_ROLES:
            if role_data["name"] not in existing_role_names:
                new_OBJ.append(dbm.Role_form(created_fk_by=emp.user_pk_id, **role_data, status=1))  # type: ignore[call-arg]

        existing_role_names = [language.language_name for language in db.query(dbm.Language_form).filter(dbm.Language_form.language_name.in_(DEFAULT_LANGUAGE)).all()]
        for language in DEFAULT_LANGUAGE:
            if language not in existing_role_names:
                UID = "7f371975-e397-4fc5-b719-75e3978fc547" if language == "Not_Assigned" else uuid.uuid4()
                new_OBJ.append(dbm.Language_form(language_pk_id=UID, created_fk_by=emp.user_pk_id, language_name=language, status=1))  # type: ignore[call-arg]

        existing_course_type = [course_type.course_type_name for course_type in db.query(dbm.Course_Type_form).filter(dbm.Course_Type_form.course_type_name.in_(DEFAULT_COURSE_TYPE)).all()]
        for course_type in DEFAULT_COURSE_TYPE:
            if course_type not in existing_course_type:
                UID = "7f485938-f59f-401f-8859-38f59f201f3e" if course_type == "Not_Assigned" else uuid.uuid4()
                new_OBJ.append(dbm.Course_Type_form(course_type_pk_id=UID, created_fk_by=emp.user_pk_id, course_type_name=course_type, status=1))  # type: ignore[call-arg]

        if new_OBJ:
            db.bulk_save_objects(new_OBJ)
            db.commit()

        logger.info('Admin Setup Finished')
    except Exception as e:
        db.rollback()
        logger.error("Admin Setup Failed")
        logger.error(f'{e.__class__.__name__}: {e.args}')
