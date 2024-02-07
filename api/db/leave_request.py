import logging

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Exist import employee_exist


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_leave_request(db: Session):
    try:
        data = db.query(dbm.Leave_request_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        if not employee_exist(db, [Form.created_by, Form.created_for]):
            return 404, "Target Employee Not Found"
        OBJ = dbm.Leave_request_form()

        OBJ.created_by_fk_id = Form.created_by
        OBJ.created_for_fk_id = Form.created_for
        OBJ.start_date = Form.start_date
        OBJ.end_date = Form.end_date
        OBJ.Description = Form.Description

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
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=Form.leave_request_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_by, Form.created_for]):
            return 404, "Target Employee Not Found"

        record.created_by_fk_id = Form.created_by
        record.created_for_fk_id = Form.created_for
        record.Start_Date = Form.start_date,
        record.End_Date = Form.end_date,
        record.Description = Form.Description
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
