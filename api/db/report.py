from lib import logger


from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *

from .fingerprint_scanner import report_fingerprint_scanner
from .remote_request import report_remote_request
from .leave_request import report_leave_request
from .business_trip import report_business_trip


def get_payment_method(db: Session, salary_report: sch.salary_report):
    try:
        salary = db.query(dbm.SalaryPolicy_form).filter_by(deleted=False, employee_fk_id=salary_report.employee_fk_id).first()
        if not salary:
            return 400, "Bad Request: Target Employee has no salary record"

        start, end = generate_month_interval(salary_report.year, salary_report.month)
        EnNo = db.query(dbm.Employees_form).filter_by(deleted=False, employees_pk_id=salary_report.employee_fk_id).first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"

        F = report_fingerprint_scanner(db, salary, EnNo, start, end)
        R = report_remote_request(db, salary, salary_report.employee_fk_id, start, end)
        L = report_leave_request(db, salary, salary_report.employee_fk_id, start, end)
        B = report_business_trip(db, salary, salary_report.employee_fk_id, start, end)

        tmp = {}
        for s, i in [F, R, L, B]:
            if s == 200:
                tmp |= i
            else:
                print(i)
                return s, i

            return 200, tmp
    except Exception as e:
        logger.error(e)
        return 500, e.__repr__()