from lib import logger

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from ..Extra import *
from lib.Date_Time import generate_month_interval

from ..Employee_Forms import report_leave_request, report_remote_request, report_business_trip, report_fingerprint_scanner


def employee_salary_report(db: Session, user_fk_id, year, month):
    try:
        Salary_Policy = db.query(dbm.Salary_Policy_form).filter_by(deleted=False, user_fk_id=user_fk_id).first()
        if not Salary_Policy:
            return 400, "Bad Request: Target Employee has no salary record"

        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        EnNo = db.query(dbm.User_form).filter_by(deleted=False, user_pk_id=user_fk_id).first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"

        report_summery = report_fingerprint_scanner(db, Salary_Policy, EnNo, start, end)

        if isinstance(report_summery, str):
            return 400, report_summery
        # days_metadata = report_summery.pop('Days') if "Days" in report_summery else {"detail": "No data for Day Report"}

        report_summery |= report_remote_request(db, Salary_Policy, user_fk_id, start, end)
        report_summery |= report_leave_request(db, Salary_Policy, user_fk_id, start, end)
        report_summery |= report_business_trip(db, Salary_Policy, user_fk_id, start, end)

        report_summery["total_earning"] = sum(report_summery[key] for key in [key for key in report_summery.keys() if "earning" in key])

        # salary_obj = dbm.Salary_form(user_fk_id=user_fk_id, Days=days_metadata, Salary_Policy=Salary_Policy.summery(), **report_summery)  # type: ignore[call-arg]
        # db.add(salary_obj)
        # db.commit()

        # return 200, db.query(dbm.Salary_form).filter_by(deleted=False, salary_pk_id=salary_obj.salary_pk_id).first()
        return 200, report_summery
    except Exception as e:
        return Return_Exception(db, e)


@not_implemented
def teacher_salary_report(db: Session, Form: sch.teacher_salary_report, year, month):
    try:
        start, end = generate_month_interval(year, month)
        return 200, start
    except Exception as e:
        return Return_Exception(db, e)
