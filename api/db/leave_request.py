import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=form_id,deleted=False).first()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_leave_request(db: Session):
    try:
        return 200, db.query(dbm.Leave_request_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        if not employee_exist(db, [Form.created_by, Form.created_for]):
            return 400, "Bad Request"
        OBJ = dbm.Leave_request_form()

        OBJ.created_fk_by = Form.created_by
        OBJ.employee_fk_id = Form.created_for
        OBJ.start_date = Form.start_date
        OBJ.end_date = Form.end_date
        OBJ.description = Form.description

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=form_id,deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(leave_request_pk_id=Form.leave_request_id,deleted=False).first()
        if not record:
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_by, Form.created_for]):
            return 400, "Bad Request"

        record.created_fk_by = Form.created_by
        record.employee_fk_id = Form.created_for
        record.Start_Date = Form.start_date,
        record.End_Date = Form.end_date,
        record.description = Form.description
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
