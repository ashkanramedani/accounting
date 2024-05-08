import uuid

from lib import logger
from sqlalchemy.orm import Session
import db.models as dbm


def setUp_admin(db: Session):
    try:
        emp = db.query(dbm.User_form).filter_by(name="Admin").first()
        if not emp:
            UID = uuid.uuid4()


            OBJ = dbm.User_form(user_pk_id=UID, created_fk_by=UID, name="Admin", last_name="Admin")  # type: ignore[call-arg]
            db.add(OBJ)
            db.commit()
            db.refresh(OBJ)
            emp = db.query(dbm.User_form).filter_by(name="Admin").first()

            if not db.query(dbm.Role_form).filter_by(name="Administrator").first():
                OBJ = dbm.Role_form(created_fk_by=emp.user_pk_id, name="Administrator", cluster="Administrator")  # type: ignore[call-arg]
                db.add(OBJ)
                db.commit()
                db.refresh(OBJ)

            emp.roles.append(db.query(dbm.Role_form).filter_by(name="Administrator").first())
            db.commit()
        logger.info(f'Admin Setup Finished')
    except Exception as e:
        db.rollback()
        logger.error("Admin Setup Failed")
        logger.error(f'{e.__class__.__name__}: {e.args}')
