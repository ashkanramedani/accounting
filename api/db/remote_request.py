import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# remote_request
def get_remote_request_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_remote_request_form(db: Session):
    try:
        return 200, db.query(dbm.Remote_Request_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_remote_request_form(db: Session, Form: sch.post_remote_request_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        OBJ = dbm.Remote_Request_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_remote_request_form(db: Session, form_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_remote_request_form(db: Session, Form: sch.update_remote_request_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=Form.remote_request_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.employee_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        data["update_date"] = datetime.now(timezone.utc).astimezone()
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
