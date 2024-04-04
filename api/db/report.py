from lib import logger


from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *

from .fingerprint_scanner import report_fingerprint_scanner
from .remote_request import report_remote_request
from .leave_request import report_leave_request
from .business_trip import report_business_trip


def get_report(db: Session, employee_fk_id, year, month):
    try:
        salary = db.query(dbm.SalaryPolicy_form).filter_by(deleted=False, employee_fk_id=employee_fk_id).first()
        if not salary:
            return 400, "Bad Request: Target Employee has no salary record"

        start, end = generate_month_interval(year, month)
        EnNo = db.query(dbm.Employees_form).filter_by(deleted=False, employees_pk_id=employee_fk_id).first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"

        F = report_fingerprint_scanner(db, salary, EnNo, start, end)
        R = report_remote_request(db, salary, employee_fk_id, start, end)
        L = report_leave_request(db, salary, employee_fk_id, start, end)
        B = report_business_trip(db, salary, employee_fk_id, start, end)

        tmp = {}
        for s, i in [F, R, L, B]:
            if s == 200:
                tmp |= i
            else:
                logger.warning(i)
                return s, i

        days_metadata = tmp.pop('Days')
        salary_obj = dbm.Salary(employee_fk_id=employee_fk_id, day_report_summery=days_metadata, salary_policy_summery=salary.summery(), **tmp)  # type: ignore[call-arg]
        db.add(salary_obj)
        db.commit()

        return 200, tmp
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()