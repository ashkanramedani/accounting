from sqlalchemy import func

from lib import logger

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from ..Extra import *
from lib.Date_Time import generate_month_interval

from ..Employee_Forms import report_leave_request, report_remote_request, report_business_trip, report_fingerprint_scanner
from ..Teacher_Forms import *
from ..Course import course_report

"""
{
  "detail": "ProgrammingError: ('(
  psycopg2.errors.GroupingError
  column \"fingerprint_scanner.priority\" must appear in the GROUP BY clause or be used in an aggregate function\\nLINE 1: SELECT fingerprint_scanner.priority AS fingerprint_scanner_p...\\n               ^\\n',)"
}
"""


def employee_salary(db: Session, year, month):
    try:
        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        Finger_Scanner_Result: list = db \
            .query(dbm.Fingerprint_Scanner_form.EnNo) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start, end)) \
            .filter_by(deleted=False) \
            .distinct() \
            .all()

        Unique_EnNo = [result.EnNo for result in Finger_Scanner_Result]

        salaries = db \
            .query(dbm.Employee_Salary_form.user_fk_id) \
            .filter_by(year=year, month=month, deleted=False) \
            .filter(dbm.Employee_Salary_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .all()
        Salary_Result = [obj[0] for obj in salaries]

        # for user in Finger_Scanner_Result:
        #     user

        return 200, {"Unique_EnNo": Unique_EnNo, "Salary_Result": Salary_Result}
    except Exception as e:
        return Return_Exception(db, e)


def employee_salary_report(db: Session, user_fk_id, year, month):
    try:
        Salary_Policy = db.query(dbm.Salary_Policy_form).filter_by(deleted=False, user_fk_id=user_fk_id).first()
        if not Salary_Policy:
            return 400, "Bad Request: Target Employee has no salary record"

        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        EnNo = db.query(dbm.User_form).filter_by(deleted=False, user_pk_id=user_fk_id).first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"

        report_summary = report_fingerprint_scanner(db, Salary_Policy, EnNo, start, end)

        if isinstance(report_summary, str):
            return 400, report_summary
        # days_metadata = report_summary.pop('Days') if "Days" in report_summary else {"detail": "No data for Day Report"}

        report_summary |= report_remote_request(db, Salary_Policy, user_fk_id, start, end)
        report_summary |= report_leave_request(db, Salary_Policy, user_fk_id, start, end)
        report_summary |= report_business_trip(db, Salary_Policy, user_fk_id, start, end)

        report_summary["total_earning"] = sum(report_summary[key] for key in [key for key in report_summary.keys() if "earning" in key])

        # salary_obj = dbm.Employee_Salary_form(user_fk_id=user_fk_id, Days=days_metadata, Salary_Policy=Salary_Policy.summery(), **report_summary)  # type: ignore[call-arg]
        # db.add(salary_obj)
        # db.commit()

        # return 200, db.query(dbm.Employee_Salary_form).filter_by(deleted=False, salary_pk_id=salary_obj.salary_pk_id).first()
        return 200, report_summary
    except Exception as e:
        return Return_Exception(db, e)


def teacher_salary_report(db: Session, course_id, year, month):
    try:
        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        report_summary = course_report(db, course_id)

        return 200, start
    except Exception as e:
        return Return_Exception(db, e)

"""
{
  "detail": "ProgrammingError: ('(psycopg2.errors.UndefinedFunction) operator does not exist: character varying = integer\\nLINE 3: ...e AND employee_salary.fingerprint_scanner_user_id IN (5, 4, ...\\n                                                             ^\\nHINT:  No operator matches the given name and argument types. You might need to add explicit type casts.\\n',)"
}
"""