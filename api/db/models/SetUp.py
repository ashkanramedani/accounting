import uuid

from lib import logger
from sqlalchemy.orm import Session
import db.models as dbm

ADMIN = {"name": "Admin", "lastname": "Admin", "role": {"name": "Administrator", "cluster": "Administrator"}}

DEFAULT_ROLES = [
    {"name": "Manager", "cluster": "Manager"},
    {"name": "Unknown", "cluster": "Users"},
    {"name": "Student", "cluster": "Users"},
    {"name": "Support", "cluster": "Supports"},
    {"name": "Teacher", "cluster": "Teachers"}
]


def setUp_admin(db: Session):
    try:
        emp = db.query(dbm.User_form).filter_by(name=ADMIN["name"]).first()
        if not emp:
            UID = uuid.uuid4()
            admin_user = dbm.User_form(user_pk_id=UID, created_fk_by=UID, name=ADMIN["name"], last_name=ADMIN["lastname"], status=1)  # type: ignore[call-arg]
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

        existing_roles = db.query(dbm.Role_form).filter(dbm.Role_form.name.in_([r["name"] for r in DEFAULT_ROLES])).all()
        existing_role_names = [role.name for role in existing_roles]

        new_roles = []
        for role_data in DEFAULT_ROLES:
            if role_data["name"] not in existing_role_names:
                new_roles.append(dbm.Role_form(created_fk_by=emp.user_pk_id, **role_data, status=1))  # type: ignore[call-arg]

        if new_roles:
            db.bulk_save_objects(new_roles)
            db.commit()

        logger.info('Admin Setup Finished')
    except Exception as e:
        db.rollback()
        logger.error("Admin Setup Failed")
        logger.error(f'{e.__class__.__name__}: {e.args}')
