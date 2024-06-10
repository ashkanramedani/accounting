from datetime import timedelta
from typing import Tuple, Dict

from lib import logger, Fix_datetime

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from ..Extra import *


# remote_request
def get_remote_request_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_remote_request_form(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Remote_Request_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_remote_request(db: Session, user_fk_id, start_date, end_date):
    try:
        Remote_Request_report = db.query(dbm.Remote_Request_form) \
            .filter_by(deleted=False, user_fk_id=user_fk_id) \
            .filter(dbm.Remote_Request_form.end_date.between(start_date, end_date)) \
            .all()

        return 200, Remote_Request_report
    except Exception as e:
        return Return_Exception(db, e)


def post_remote_request_form(db: Session, Form: sch.post_remote_request_schema):
    try:
        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        Start, End = Fix_datetime(data["start_date"]), Fix_datetime(data["end_date"])

        if End < Start:
            return 400, "Bad Request: End Date must be greater than Start Date"

        OBJ = dbm.Remote_Request_form(duration=(End - Start).total_seconds() // 60, **data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


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
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_remote_request_form(db: Session, Form: sch.update_remote_request_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=Form.remote_request_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

def Verify_remote_request(db: Session, Form: sch.Verify_remote_request_schema):
    try:
        Warn = []
        verified = 0
        records = db.query(dbm.Remote_Request_form) \
            .filter_by(deleted=False) \
            .filter(dbm.Remote_Request_form.remote_request_pk_id.in_(Form.remote_request_id)) \
            .all()

        for record in records:
            record.status = 1
            verified += 1

        db.commit()
        if Warn:
            return 200, f"{verified} Form Verified. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Verified."
    except Exception as e:
        return Return_Exception(db, e)