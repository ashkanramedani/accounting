from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from .Extra import *


def get_all_cluster(db: Session):
    try:
        return 200, [dict(name)["cluster"] for name in db.query(dbm.Role_form.cluster).group_by(dbm.Role_form.cluster).all()]
        # return 200, record_order_by(db, dbm.Tag_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


# role

def get_role(db: Session, role_id):
    try:
        return 200, db.query(dbm.Role_form).filter_by(role_pk_id=role_id, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_role(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Role_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


def post_role(db: Session, Form: sch.post_role_schema):
    try:

        data = Form.dict()
        if data["name"] == "Administrator":
            return 400, "illegal name Administrator"

        OBJ = dbm.Role_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_role(db: Session, role_id):
    try:
        record = db.query(dbm.Role_form).filter_by(role_pk_id=role_id, deleted=False).first()
        if not record:
            return 400, "Role Record Not Found"
        if record.name == "Administrator":
            return 400, "Administrator role cant be deleted"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_role(db: Session, Form: sch.update_role_schema):
    try:
        record = db.query(dbm.Role_form).filter_by(role_pk_id=Form.role_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        if data["name"] == "Administrator":
            return 400, "illegal name Administrator"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)
