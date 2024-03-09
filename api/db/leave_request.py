from lib import log

logger = log()

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_leave_request(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Leave_request_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.employee_fk_id]):
            return 400, "Bad Request"

        OBJ = dbm.Leave_request_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=Form.leave_request_pk_id, deleted=False)
        if not record.first():
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.employee_fk_id]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
