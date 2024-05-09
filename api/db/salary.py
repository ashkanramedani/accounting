from lib import logger



from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *
from lib.Date_Time import generate_month_interval

from .Employee_Forms import report_leave_request, report_remote_request, report_business_trip, report_fingerprint_scanner

def employee_salary_report(db: Session, user_fk_id, year, month):
    try:
        salary = db.query(dbm.Salary_Policy_form).filter_by(deleted=False, user_fk_id=user_fk_id).first()
        if not salary:
            return 400, "Bad Request: Target Employee has no salary record"
        logger.warning(f'{salary.summery() = }')

        start, end = generate_month_interval(year, month)
        EnNo = db.query(dbm.User_form).filter_by(deleted=False, user_pk_id=user_fk_id).first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"

        F = report_fingerprint_scanner(db, salary, EnNo, start, end)
        R = report_remote_request(db, salary, user_fk_id, start, end)
        L = report_leave_request(db, salary, user_fk_id, start, end)
        B = report_business_trip(db, salary, user_fk_id, start, end)

        tmp = {}
        for s, i in [F, R, L, B]:
            if s != 200:
                logger.warning(i)
                return s, i
            tmp |= i

        days_metadata = tmp.pop('Days') if "Days" in tmp else {"detail": "No data for Day Report"}


        salary_obj = dbm.Salary_form(user_fk_id=user_fk_id, day_report_summery=days_metadata, salary_policy_summery=salary.summery(), **tmp)  # type: ignore[call-arg]
        db.add(salary_obj)
        db.commit()

        return 200, "Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'



def teacher_salary_report(db: Session, Form: sch.teacher_salary_report, year, month):
    return 404 ,"not implemented"
    try:
        start, end = generate_month_interval(year, month)
        return 200, start
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

