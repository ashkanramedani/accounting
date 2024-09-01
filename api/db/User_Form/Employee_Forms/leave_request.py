from sqlalchemy.orm import Session

import schemas as sch
import models as dbm
from db.Extra import *
from lib import same_month, Separate_days_by_DayCap, is_off_day, time_gap


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=form_id).filter(dbm.Leave_Request_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_leave_request(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Leave_Request_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def report_leave_request(db: Session, user_fk_id, start_date, end_date):
    try:
        vacation_Leave_request_report = (
            db.query(dbm.Leave_Request_form)
            .filter_by(user_fk_id=user_fk_id, leave_type="vacation")
            .filter(dbm.Leave_Request_form.date.between(start_date, end_date))
            .filter(dbm.Leave_Request_form.date.between(start_date, end_date), dbm.Leave_Request_form.status != "deleted")
            .all()
        )
        medical_Leave_request_report = (
            db.query(dbm.Leave_Request_form)
            .filter_by(user_fk_id=user_fk_id, leave_type="medical")
            .filter(dbm.Leave_Request_form.date.between(start_date, end_date), dbm.Leave_Request_form.status != "deleted")
            .all()
        )

        return 200, {"Vacation": vacation_Leave_request_report, "Medical": medical_Leave_request_report}
    except Exception as e:
        return Return_Exception(db, e)


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        Warn = []
        if not employee_exist(db, [Form.created_fk_by, Form.user_fk_id]):
            return 400, "Bad Request: Employee Does Not Exist"

        data = Form.dict()

        Start, End = Fix_datetime(data.pop("start_date")), Fix_datetime(data.pop("end_date"))

        if End < Start:
            return 400, f"Bad Request: End Date must be greater than Start Date. {End} < {Start}"

        if not same_month(Start, End):
            return 400, f"Bad Request: End Date must be in the same month as Start Date: {Start}, {End}"

        # this part check if leave request is daily or hourly
        if End.date() == Start.date():
            if not is_off_day(Start):
                OBJ = dbm.Leave_Request_form(start=Start.time(), end=End.time(), duration=(End - Start).total_seconds() // 60, date=Start.date(), **data)  # type: ignore[call-arg]
                db.add(OBJ)
            else:
                Warn.append(f'Leave request for {Start.date()} not added due to holiday.')
        else:
            OBJ = []
            Salary_Obj = db.query(dbm.Salary_Policy_form).filter_by(user_fk_id=Form.user_fk_id).filter(dbm.Salary_Policy_form.status != "deleted").first()
            if not Salary_Obj:
                return 400, "Bad Request: Employee Does Not Have Employee_Salary_form Record"
            for day in Separate_days_by_DayCap(Start, End, Salary_Obj.Regular_hours_cap):
                if not day["is_holiday"]:
                    OBJ.append(dbm.Leave_Request_form(date=day["Date"], duration=day["duration"], **data))  # type: ignore[call-arg]
                else:
                    Warn.append(f'Leave request for {day["Date"]} not added due to holiday.')

            db.add_all(OBJ)
        db.commit()
        if Warn:
            return 200, f'Form Added with Warning. {" | ".join(Warn)}'
        return 200, f"Form Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=form_id).filter(dbm.Leave_Request_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_Request_form).filter_by(leave_request_pk_id=Form.leave_request_pk_id).filter(dbm.Leave_Request_form.status != "deleted")
        if not record.first():
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.__dict__
        data["duration"] = time_gap(data["start"], data["end"])
        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def Verify_leave_request(db: Session, Form: sch.Verify_leave_request_schema, status: sch.CanUpdateStatus):
    try:
        Warn = []
        verified = 0
        records = db.query(dbm.Leave_Request_form) \
            .filter(dbm.Leave_Request_form.deleted == False, dbm.Leave_Request_form.status != "deleted", dbm.Leave_Request_form.status != status, dbm.Leave_Request_form.leave_request_pk_id.in_(Form.leave_request_id)) \
            .all()

        for record in records:
            record.status = Set_Status(db, "form", status)
            verified += 1

        db.commit()
        if Warn:
            return 200, f"{verified} Form Update Status To {status}. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Update Status To {status}."
    except Exception as e:
        return Return_Exception(db, e)
