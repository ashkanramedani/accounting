from typing import Tuple, Dict

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


def report_leave_request(db: Session, salary_rate: sch.SalaryPolicy, user_fk_id, start_date, end_date) -> Dict:
    vacation_leave, medical_leave = 0, 0
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

    if vacation_Leave_request_report:
        vacation_leave = salary_rate.medical_leave_cap - sum(row.duration for row in vacation_Leave_request_report)

    if medical_Leave_request_report:
        medical_leave = salary_rate.medical_leave_cap - sum(row.duration for row in medical_Leave_request_report)

    return {
        "vacation_leave": vacation_leave,
        "vacation_leave_earning": (vacation_leave / 60) * salary_rate.vacation_leave_factor * salary_rate.Base_salary,
        "medical_leave": medical_leave,
        "medical_leave_earning": (min(medical_leave, 0) / 60) * salary_rate.medical_leave_factor * salary_rate.Base_salary}

"""
"created_fk_by": "7cdfdaf3-cb2c-48a5-b371-ae09c0c74f57",
"description": "string",
"status": 0,
"visible": true,
"priority": 5,
"can_update": true,
"can_deleted": true,
"user_fk_id": "7cdfdaf3-cb2c-48a5-b371-ae09c0c74f57",
"leave_type": "vacation",
"start_date": "2024-05-20T16:17:00.577242",
"end_date": "2024-05-21T16:17:00.577251"
"""

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
                return 400, "Bad Request: Employee Does Not Have Salary_form Record"
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
