import uuid

from sqlalchemy.orm import Session

from db import models as dbm
from lib import logger

DEFAULT_USER = [
    {
        "name": "Admin",
        "lastname": "Admin",
        "email": "Admin@Admin.com",
        "ID": "308e2744-833c-4b94-8e27-44833c2b940f",
        "role": {"name": "Administrator", "cluster": "Administrator"}
    },
    {
        "name": "Test",
        "lastname": "Teacher",
        "email": "Test@Teacher.com",
        "ID": "01909c17-48f9-0af0-6d35-70f541d47bce",
        "role": {"name": "Teacher", "cluster": "Teachers"}
    }
]

DEFAULT_ROLES = [
    {"name": "Manager", "cluster": "Manager"},
    {"name": "Unknown", "cluster": "Users"},
    {"name": "Student", "cluster": "Users"},
    {"name": "Support", "cluster": "Supports"},
    {"name": "Teacher", "cluster": "Teachers"}
]


DEFAULT_STATUS = {
    "form": [
        "submitted",
        "approved",
        "rejected",
        "pending",
        "cancelled",
        "deleted"
    ],
    "payment": []
}

DEFAULT_LANGUAGE = ["Not_Assigned", "English", "Spanish", "Italian", "French", "German", "Chinese", "Japanese", "Korean", "Portuguese", "Russian"]
DEFAULT_COURSE_TYPE = ["Not_Assigned", "Online", "Offline", "OnSite"]


def setUp_admin(db: Session):
    try:
        Existing_users = [user[0] for user in db.query(dbm.User_form.name).filter(dbm.User_form.name.in_([user["name"] for user in DEFAULT_USER])).all()]

        for User in DEFAULT_USER:
            if User["name"] in Existing_users:
                continue
            data = {"user_pk_id": User["ID"], "name": User["name"], "last_name": User["lastname"], "email": User["email"], "status": "approved"}

            admin_user = dbm.User_form(**data)  # type: ignore[call-arg]
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            admin_user.created_fk_by = "308e2744-833c-4b94-8e27-44833c2b940f"
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            emp = admin_user

            admin_role = db.query(dbm.Role_form).filter_by(name=User["role"]["name"]).first()
            if not admin_role:
                admin_role = dbm.Role_form(created_fk_by=emp.user_pk_id, name=User["role"]["name"], cluster=User["role"]["cluster"], status="approved")  # type: ignore[call-arg]
                db.add(admin_role)
                db.commit()

            emp.roles.append(admin_role)

        ADMIN_ID = db.query(dbm.User_form).filter_by(name="Admin").first().user_pk_id
        existing_role_names = [role.name for role in db.query(dbm.Role_form).filter(dbm.Role_form.name.in_([r["name"] for r in DEFAULT_ROLES])).all()]
        new_OBJ = []

        for role_data in DEFAULT_ROLES:
            if role_data["name"] not in existing_role_names:
                OBJ = dbm.Role_form(created_fk_by=ADMIN_ID, status="approved", **role_data)  # type: ignore[call-arg]
                new_OBJ.append(OBJ)

        existing_role_names = [language.language_name for language in db.query(dbm.Language_form).filter(dbm.Language_form.language_name.in_(DEFAULT_LANGUAGE)).all()]
        for language in DEFAULT_LANGUAGE:
            if language not in existing_role_names:
                UID = "7f371975-e397-4fc5-b719-75e3978fc547" if language == "Not_Assigned" else uuid.uuid4()
                OBJ = dbm.Language_form(language_pk_id=UID, created_fk_by=ADMIN_ID, language_name=language, status="approved")  # type: ignore[call-arg]
                new_OBJ.append(OBJ)

        existing_course_type = [course_type.course_type_name for course_type in db.query(dbm.Course_Type_form).filter(dbm.Course_Type_form.course_type_name.in_(DEFAULT_COURSE_TYPE)).all()]
        for course_type in DEFAULT_COURSE_TYPE:
            if course_type not in existing_course_type:
                UID = "7f485938-f59f-401f-8859-38f59f201f3e" if course_type == "Not_Assigned" else uuid.uuid4()
                OBJ = dbm.Course_Type_form(course_type_pk_id=UID, created_fk_by=ADMIN_ID, course_type_name=course_type, status="approved")  # type: ignore[call-arg]
                new_OBJ.append(OBJ)

        if new_OBJ:
            db.bulk_save_objects(new_OBJ)
            db.commit()

        logger.info('Admin Setup Finished')
    except Exception as e:
        db.rollback()
        logger.error("Admin Setup Failed")
        logger.error(f'{e.__class__.__name__}: {e.args}')
