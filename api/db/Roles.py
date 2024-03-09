from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import log
from .Extra import *

logger = log()


# role
def get_role(db: Session, role_id):
    try:
        return 200, db.query(dbm.Roles_form).filter_by(role_pk_id=role_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_role(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Roles_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_role(db: Session, Form: sch.post_role_schema):
    try:
        OBJ = dbm.Roles_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_role(db: Session, role_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(role_id_pk_id=role_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_role(db: Session, Form: sch.update_role_schema):
    try:
        record = db.query(dbm.Roles_form).filter_by(role_pk_id=Form.role_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
