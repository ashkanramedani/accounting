import logging
from uuid import UUID
from .Exist import employee_exist
from sqlalchemy.orm import Session
from typing import List
import schemas as sch
import db.models as dbm
from .Exist import employee_exist

# remote_request
def get_remote_request_form(db: Session, form_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_remote_request_form(db: Session):
    try:
        data = db.query(dbm.Remote_Request_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_remote_request_form(db: Session, Form: sch.post_remote_request_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        OBJ = dbm.Remote_Request_form(
                employee_fk_id=Form.employee_fk_id,
                start_date=Form.start_date,
                end_date=Form.end_date,
                working_location=Form.working_location,
                description=Form.description
        )
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
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_remote_request_form(db: Session, Form: sch.update_remote_request_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=Form.remote_request_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        record.employee_fk_id = Form.employee_fk_id,
        record.start_date = Form.start_date,
        record.end_date = Form.end_date,
        record.working_location = Form.working_location,
        record.description = Form.description

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
