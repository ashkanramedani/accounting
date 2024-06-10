from typing import Tuple, Dict
from datetime import time
from lib import logger, Fix_datetime, same_month, Separate_days_by_DayCap, is_off_day

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from ..Extra import *


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_leave_request(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Leave_Request_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_leave_request(db: Session, user_fk_id, start_date, end_date):
    try:
        vacation_Leave_request_report = (
            db.query(dbm.Leave_Request_form)
            .filter_by(deleted=False, user_fk_id=user_fk_id, leave_type="vacation")
            .filter(dbm.Leave_Request_form.date.between(start_date, end_date))
            .all()
        )
        medical_Leave_request_report = (
            db.query(dbm.Leave_Request_form)
            .filter_by(deleted=False, user_fk_id=user_fk_id, leave_type="medical")
            .filter(dbm.Leave_Request_form.date.between(start_date, end_date))
            .all()
        )

        return 200, {"Vacation": vacation_Leave_request_report, "Medical": medical_Leave_request_report}
    except Exception as e:
        return Return_Exception(db, e)


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.user_fk_id]):
            return 400, "Bad Request: Employee Does Not Exist"

        data = Form.dict()

        Start, End = Fix_datetime(data.pop("start_date")), Fix_datetime(data.pop("end_date"))

        if End < Start:
            return 400, "Bad Request: End Date must be greater than Start Date"

        if not same_month(Start, End):
            return 400, f"Bad Request: End Date must be in the same month as Start Date: {Start}, {End}"

        # this part check if leave request is daily or hourly
        if End.date() == Start.date():
            if not is_off_day(Start):
                OBJ = dbm.Leave_Request_form(start_date=Start.time(), end_date=End.time(), duration=(End - Start).total_seconds() // 60, date=Start.replace(hour=0, minute=0, second=0, microsecond=0), **data)  # type: ignore[call-arg]
                db.add(OBJ)
        else:
            OBJ = []
            Salary_Obj = db.query(dbm.Salary_Policy_form).filter_by(user_fk_id=Form.user_fk_id, deleted=False).first()
            if not Salary_Obj:
                return 400, "Bad Request: Employee Does Not Have Employee_Salary_form Record"
            for day in Separate_days_by_DayCap(Start, End, Salary_Obj.Regular_hours_cap):
                if not day["is_holiday"]:
                    OBJ.append(dbm.Leave_Request_form(start_date=time(0, 0, 0), end_date=time(24, 59, 59), date=day["Date"], duration=day["duration"], **data))  # type: ignore[call-arg]

            db.add_all(OBJ)
        db.commit()

        return 200, f"Form Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=Form.leave_request_pk_id, deleted=False)
        if not record.first():
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.user_fk_id]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def Verify_leave_request(db: Session, Form: sch.Verify_leave_request_schema):
    try:
        Warn = []
        verified = 0
        records = db.query(dbm.Leave_Request_form) \
            .filter_by(deleted=False) \
            .filter(dbm.Leave_Request_form.leave_request_pk_id.in_(Form.leave_request_id)) \
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
