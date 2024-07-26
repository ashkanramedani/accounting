import dbm
import json

from db.Course import course_report
from db.User_Form import *


def permissions(db: Session, User_ID):
    try:
        permission = db \
            .query(dbm.Salary_Policy_form.remote_permission, dbm.Salary_Policy_form.business_trip_permission) \
            .filter_by(user_fk_id=User_ID).filter(dbm.Salary_Policy_form.status != "deleted") \
            .order_by(dbm.Salary_Policy_form.create_date.desc()) \
            .first()

        if not permission:
            return 200, {"remote_permission": False, "business_trip_permission": False, "salary_Policy": False}

        return 200, {**permission, "salary_Policy": True}
    except Exception as e:
        return Return_Exception(db, e)


def employee_salary(db: Session, year, month):  # NC: 003
    try:
        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)
        Finger_Scanner_Result: list = db \
            .query(dbm.Fingerprint_Scanner_form.EnNo) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start, end)) \
            .filter(dbm.Fingerprint_Scanner_form.status != "deleted") \
            .distinct() \
            .all()

        Unique_EnNo = [result.EnNo for result in Finger_Scanner_Result]

        users_with_fingerprints = db.query(dbm.User_form) \
            .filter(dbm.User_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .filter(dbm.User_form.status != "deleted") \
            .all()

        salaries = db \
            .query(dbm.Employee_Salary_form.fingerprint_scanner_user_id) \
            .filter_by(year=year, month=month).filter(dbm.Employee_Salary_form.status != "deleted") \
            .filter(dbm.Employee_Salary_form.fingerprint_scanner_user_id.in_(Unique_EnNo)) \
            .all()

        Salary_Result = [obj[0] for obj in salaries]

        Salry_policies = db \
            .query(dbm.Salary_Policy_form.user_fk_id) \
            .filter(dbm.Salary_Policy_form.status != "deleted", dbm.Salary_Policy_form.user_fk_id.in_([user.user_pk_id for user in users_with_fingerprints])) \
            .all()

        Salary_Policy_Result = [obj[0] for obj in Salry_policies]

        Result = []
        for user in users_with_fingerprints:
            data = user.__dict__
            data["Does_Have_Salary_Record"] = user.fingerprint_scanner_user_id in Salary_Result
            data["Does_Have_Salary_Policy"] = user.user_pk_id in Salary_Policy_Result
            Result.append(data)

        return 200, Result
    except Exception as e:
        return Return_Exception(db, e)


def Get_Report(db: Session, Salary_Policy: dbm.Salary_Policy_form, user_fk_id: UUID, start, end) -> Dict:
    Remote_Request_report = []
    Business_Trip_report = []

    # Remote
    if Salary_Policy.remote_permission:
        Remote_Request_report: List = db \
            .query(dbm.Remote_Request_form.date, func.sum(dbm.Remote_Request_form.duration).label('duration')) \
            .filter_by(user_fk_id=user_fk_id).filter(dbm.Remote_Request_form.status != "deleted") \
            .filter(dbm.Remote_Request_form.date.between(start, end)) \
            .group_by(dbm.Remote_Request_form.date) \
            .all()

    if Salary_Policy.business_trip_permission:
        Business_Trip_report: List = db \
            .query(dbm.Business_Trip_form.date, func.sum(dbm.Business_Trip_form.duration).label('duration')) \
            .filter_by(user_fk_id=user_fk_id).filter(dbm.Business_Trip_form.status != "deleted") \
            .filter(dbm.Business_Trip_form.date.between(start, end)) \
            .group_by(dbm.Business_Trip_form.date) \
            .all()

    Vacation_leave_report: List = db \
        .query(dbm.Leave_Request_form.date, func.sum(dbm.Leave_Request_form.duration).label('duration')) \
        .filter_by(user_fk_id=user_fk_id, leave_type="vacation").filter(dbm.Leave_Request_form.status != "deleted") \
        .filter(dbm.Leave_Request_form.date.between(start, end)) \
        .group_by(dbm.Leave_Request_form.date) \
        .all()

    Medical_leave_report: List = db \
        .query(dbm.Leave_Request_form.date, func.sum(dbm.Leave_Request_form.duration).label('duration')) \
        .filter_by(user_fk_id=user_fk_id, leave_type="medical").filter(dbm.Leave_Request_form.status != "deleted") \
        .filter(dbm.Leave_Request_form.date.between(start, end)) \
        .group_by(dbm.Leave_Request_form.date) \
        .all()

    return {
        "remote":
            {str(record["date"]): record["duration"] for record in Remote_Request_report},
        "business_trip":
            {str(record["date"]): record["duration"] for record in Business_Trip_report},
        "vacation_leave":
            {str(record["date"]): record["duration"] for record in Vacation_leave_report},
        "medical_leave":
            {str(record["date"]): record["duration"] for record in Medical_leave_report},
    }


def employee_salary_report(db: Session, user_fk_id, year, month):

    try:
        existing = db.query(dbm.Employee_Salary_form).filter_by(user_fk_id=user_fk_id, year=year, month=month).filter(dbm.Employee_Salary_form.status != "deleted").first()
        if existing:
            return 200, existing
        Salary_Policy = db \
            .query(dbm.Salary_Policy_form) \
            .filter_by(user_fk_id=user_fk_id) \
            .filter(dbm.Salary_Policy_form.status != "deleted") \
            .order_by(dbm.Salary_Policy_form.create_date.desc()) \
            .first()

        if not Salary_Policy:
            return 400, "Bad Request: Target Employee has no salary record"

        start, end = generate_month_interval(year, month, include_nex_month_fist_day=True)


        EnNo = db.query(dbm.User_form).filter_by(user_pk_id=user_fk_id).filter(dbm.User_form.status != "deleted").first().fingerprint_scanner_user_id
        if EnNo is None:
            return 400, "Bad Request: Target Employee Has no fingerprint scanner ID"


        status, report_summary = report_fingerprint_scanner(db, EnNo, start, end)
        if status != 200:
            return status, report_summary

        if report_summary["Invalid"] != 0:
            return 400, "Invalid Date Found."

        status, report_summary = generate_daily_report(
                Salary_Policy=Salary_Policy,
                Fingerprint_scanner_report=report_summary["Fingerprint_scanner_report"],
                Activities=Get_Report(db, Salary_Policy, user_fk_id, start, end))


        if status != 200:
            return status, report_summary

        days_metadata = report_summary.pop('Days') if "Days" in report_summary else {"detail": "No data for Day Report"}

        salary_obj = dbm.Employee_Salary_form(user_fk_id=user_fk_id, year=year, month=month, fingerprint_scanner_user_id=EnNo, Days=days_metadata, Salary_Policy=Salary_Policy.summery(), **report_summary)  # type: ignore[call-arg]

        db.add(salary_obj)
        db.commit()
        db.refresh(salary_obj)

        return 200, salary_obj
    except Exception as e:
        return Return_Exception(db, e)


def get_employee_salary(db: Session, user_fk_id, year, month):
    try:
        return 200, db.query(dbm.Employee_Salary_form).filter_by(user_fk_id=user_fk_id, year=year, month=month).filter(dbm.Employee_Salary_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)