from lib.Date_Time import generate_month_interval

from ..Course import course_report
from ..Employee_Forms import report_leave_request, report_remote_request, report_business_trip, report_fingerprint_scanner
from ..Teacher_Forms import *


def employee_salary(db: Session, year, month):  # NC: 003
    try:
        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        Finger_Scanner_Result: list = db \
            .query(dbm.Fingerprint_Scanner_form.EnNo) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start, end)) \
            .filter_by(deleted=False) \
            .distinct() \
            .all()

        Unique_EnNo = [result.EnNo for result in Finger_Scanner_Result]

        users_with_fingerprints = db.query(dbm.User_form) \
            .filter(dbm.User_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .all()

        salaries = db \
            .query(dbm.Employee_Salary_form.user_fk_id) \
            .filter_by(year=year, month=month, deleted=False) \
            .filter(dbm.Employee_Salary_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .all()

        Salary_Result = [obj[0] for obj in salaries]

        Result = []
        for user in users_with_fingerprints:
            data = user.__dict__
            data["Does_Have_Salary_Record"] = user.fingerprint_scanner_user_id in Salary_Result
            Result.append(data)

        return 200, Result
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

        salary_obj = dbm.Employee_Salary_form(user_fk_id=user_fk_id, Days=days_metadata, Salary_Policy=Salary_Policy.summery(), **report_summary)  # type: ignore[call-arg]
        db.add(salary_obj)
        db.commit()
        db.refresh(salary_obj)

        # return 200, db.query(dbm.Employee_Salary_form).filter_by(deleted=False, salary_pk_id=salary_obj.salary_pk_id).first()
        return 200, report_summary
    except Exception as e:
        return Return_Exception(db, e)


def teacher_salary_report(db: Session, Form: sch.teacher_salary_report):
    try:
        status, report_summary = course_report(db, Form.course_id, Form.Cancellation_factor)
        return status, report_summary
    except Exception as e:
        return Return_Exception(db, e)
