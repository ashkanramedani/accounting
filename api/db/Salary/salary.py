from lib.Date_Time import generate_month_interval
from .. import generate_daily_report

from ..Course import course_report
from ..Employee_Forms import report_leave_request, report_remote_request, report_business_trip, report_fingerprint_scanner
from ..Teacher_Forms import *


def permissions(db: Session, User_ID):
    try:
        return 200, db. \
            query(dbm.Salary_Policy_form.remote_permission, dbm.Salary_Policy_form.business_trip_permission) \
            .filter_by(user_fk_id=User_ID, deleted=False) \
            .order_by(dbm.Salary_Policy_form.create_date.desc()) \
            .first()
    except Exception as e:
        return Return_Exception(db, e)


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
            .filter_by(deleted=False) \
            .all()

        salaries = db \
            .query(dbm.Employee_Salary_form.fingerprint_scanner_user_id) \
            .filter_by(year=year, month=month, deleted=False) \
            .filter(dbm.Employee_Salary_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .all()

        Salary_Result = [obj[0] for obj in salaries]

        Result = []
        for user in users_with_fingerprints:
            data = user.__dict__
            data["Does_Have_Salary_Record"] = user.fingerprint_scanner_user_id in Salary_Result
            Result.append(data)

        logger.warning({i["name"]: i["Does_Have_Salary_Record"] for i in Result})

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

        status, report_summary = report_fingerprint_scanner(db, EnNo, start, end)
        if status != 200:
            return status, report_summary

        status, report_summary = generate_daily_report(Salary_Policy, report_summary)

        if status != 200:
            return status, report_summary

        days_metadata = report_summary.pop('Days') if "Days" in report_summary else {"detail": "No data for Day Report"}

        # Remote Request
        if Salary_Policy.remote_permission:
            status, Remote_Request_report = report_remote_request(db, user_fk_id, start, end)
            if status != 200:
                return status, Remote_Request_report
            total_remote = sum(row.duration for row in Remote_Request_report)
            remote = min(total_remote, Salary_Policy.remote_cap)
            report_summary |= {"remote": remote, "remote_earning": (remote / 60) * Salary_Policy.remote_factor * Salary_Policy.Base_salary}
        else:
            report_summary |= {"remote": 0, "remote_earning": 0}

        # Business Trip
        if Salary_Policy.business_trip_permission:
            status, Business_Trip_report = report_business_trip(db, user_fk_id, start, end)
            if status != 200:
                return status, Business_Trip_report
            total_business_trip = sum(row.duration for row in Business_Trip_report)
            business_trip = min(total_business_trip, Salary_Policy.business_trip_cap)
            report_summary |= {"business_trip": business_trip, "business_trip_earning": (business_trip / 60) * Salary_Policy.business_trip_factor * Salary_Policy.Base_salary}
        else:
            report_summary |= {"business_trip": 0, "business_trip_earning": 0}

        # Leave Request
        status, leave_report = report_leave_request(db, user_fk_id, start, end)
        if status != 200:
            return status, leave_report

        vacation = Salary_Policy.vacation_leave_cap - sum(row.duration for row in leave_report["Vacation"]) if leave_report["Vacation"] else 0
        medical = Salary_Policy.medical_leave_cap - sum(row.duration for row in leave_report["Medical"]) if leave_report["Medical"] else 0

        report_summary |= {
            "vacation_leave": vacation, "vacation_leave_earning": (vacation / 60) * Salary_Policy.vacation_leave_factor * Salary_Policy.Base_salary,
            "medical_leave": medical, "medical_leave_earning": (min(medical, 0) / 60) * Salary_Policy.medical_leave_factor * Salary_Policy.Base_salary}

        report_summary["total_earning"] = sum(report_summary[key] for key in [key for key in report_summary.keys() if "earning" in key])

        salary_obj = dbm.Employee_Salary_form(user_fk_id=user_fk_id, year=year, month=month, fingerprint_scanner_user_id=EnNo, Days=days_metadata, Salary_Policy=Salary_Policy.summery(), **report_summary)  # type: ignore[call-arg]
        db.add(salary_obj)
        db.commit()
        db.refresh(salary_obj)

        return 200, salary_obj
    except Exception as e:
        return Return_Exception(db, e)

def get_employee_salary(db: Session, user_fk_id, year, month):
    try:
        return 200, db.query(dbm.Employee_Salary_form).filter_by(user_fk_id=user_fk_id, year=year, month=month, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def teacher_salary_report(db: Session, Form: sch.teacher_salary_report):
    try:
        status, report_summary = course_report(db, Form.course_id, Form.Cancellation_factor)
        return status, report_summary
    except Exception as e:
        return Return_Exception(db, e)

"""
11, 6, 7, 13, 9, 10, 12, 15, 17 
6 
5, 4, 16, 15, 6, 12, 3, 17, 11, 10, 13, 9, 7
"""