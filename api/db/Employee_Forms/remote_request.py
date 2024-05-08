from datetime import timedelta
from typing import Tuple

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


def report_remote_request(db: Session, salary_rate, user_fk_id, start_date, end_date) -> Tuple[int, dict | str]:
    if not salary_rate.remote_permission:
        return 200, {"remote": 0, "remote_earning": 0}

    Remote_Request_report = (
        db.query(dbm.Remote_Request_form)
        .filter_by(deleted=False, user_fk_id=user_fk_id)
        .filter(dbm.Remote_Request_form.end_date.between(start_date, end_date))
        .all()
    )

    total_remote = sum(row.duration for row in Remote_Request_report)
    remote = min(total_remote, salary_rate.remote_cap)
    return 200, {"remote": remote, "remote_earning": remote * salary_rate.remote_factor}

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
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


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
