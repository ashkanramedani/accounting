import uuid
from datetime import timedelta, date, time, datetime

import pandas as pd
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from .Extra import *


def Date_constructor(Date_obj: str | date | datetime):
    Date_obj = Fix_date(Date_obj)
    if Date_obj.year > 2000:
        M_Date = Date_obj
        P_Date = to_persian(Date_obj.year, Date_obj.month, Date_obj.day)
    else:
        M_Date = to_international(Date_obj.year, Date_obj.month, Date_obj.day)
        P_Date = Date_obj
    return f'{M_Date}  {P_Date}'


def preprocess_report(report):
    preprocess_Days = {}
    for record in report:
        Key = str(record["Date"])
        if record["Enter"] is None or record["Exit"] is None:
            preprocess_Days[Key] = {"TotalWork": 0, "EnterExit": [record["Enter"], record["Exit"]], "IsValid": False, "msg": 'invalid Enter/exit time'}
            continue
        if record["Date"] not in preprocess_Days:
            preprocess_Days[Key] = {"TotalWork": 0, "EnterExit": [], "IsValid": True, "msg": "Processed"}

        preprocess_Days[Key]["TotalWork"] += _sub(record["Enter"], record["Exit"])
        preprocess_Days[Key]["EnterExit"].append(record["Enter"])
        preprocess_Days[Key]["EnterExit"].append(record["Exit"])
    return preprocess_Days


def Fixed_schedule(EMP_Salary: dbm.SalaryPolicy_form, report):
    preprocess_Days = preprocess_report(report)
    Days = []
    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))

        Overtime, Undertime, Regular_hours, off_day_overtime, TotalWork = 0, 0, 0, 0, 0
        if not day["IsValid"]:
            Days.append({
                "Date": Date_constructor(Date),
                "Holiday": Holiday,
                "Total Work": 0,
                "Regular_hours": 0,
                "Overtime": 0,
                "Undertime": 0,
                "off_Day_Overtime": 0,
                "IsValid": False,
                "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]),
                "msg": day["msg"]})
            continue

        if Holiday:
            if EMP_Salary.off_day_permission:
                off_day_overtime = day["TotalWork"]

        else:
            first_enter: time = max(min(day["EnterExit"]), EMP_Salary.day_starting_time)  # type: ignore
            last_exit: time = max(day["EnterExit"])  # type: ignore
            # UnderTime
            tmp_undertime = _sub(EMP_Salary.day_starting_time, first_enter)
            Undertime = tmp_undertime if tmp_undertime > EMP_Salary.undertime_threshold else 0

            if last_exit < EMP_Salary.day_ending_time:
                tmp_undertime = _sub(last_exit, EMP_Salary.day_ending_time)
                Undertime += tmp_undertime if tmp_undertime > EMP_Salary.undertime_threshold else 0
            else:
                tmp_overtime = _sub(EMP_Salary.day_ending_time, last_exit)
                Overtime = tmp_overtime if tmp_overtime > EMP_Salary.overtime_threshold else 0
                # Overtime = min(Overtime, EMP_Salary.overtime_cap) # Cap has been moved to total (Monthly)

            EnterExit = day["EnterExit"]
            EnterExit.sort()
            enters = EnterExit[2::2]
            exits = EnterExit[1:-1:2]
            # check if more than one Enter and Exit is in day
            if len(EnterExit) != 2:
                for Enter, Exit in zip(enters, exits):
                    day["Undertime"] += _sub(Enter, Exit)

        Days.append({
            "Date": Date_constructor(Date),
            "Holiday": Holiday,
            "TotalWork": day["TotalWork"],
            "Regular_hours": min(day["TotalWork"] - Overtime, EMP_Salary.Regular_hours_cap),
            "Overtime": Overtime,
            "Undertime": Undertime,
            "off_Day_Overtime": off_day_overtime,
            "IsValid": True,
            "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]),
            "msg": "Finished"})
    return Days


def Split_schedule(EMP_Salary, reports):
    preprocess_Days = preprocess_report(reports)
    Days = []

    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))
        Overtime, Undertime, Regular_hours, off_day_overtime = 0, 0, 0, 0
        if not day["IsValid"]:
            Days.append({
                "Date": Date_constructor(Date),
                "Holiday": Holiday,
                "Total Work": 0,
                "Regular_hours": 0,
                "Overtime": 0,
                "Undertime": 0,
                "off_Day_Overtime": 0,
                "IsValid": False,
                "EnterExit": '-'.join([str(t) for t in day["EnterExit"]]),
                "msg": day["msg"]})
            continue

        if Holiday:
            if EMP_Salary.off_day_permission:
                off_day_overtime = day["TotalWork"]
        else:
            TotalWork = day["TotalWork"]

            if TotalWork >= EMP_Salary.Regular_hours_cap:
                posible_Overtime = TotalWork - EMP_Salary.Regular_hours_cap
                Overtime = posible_Overtime if posible_Overtime >= EMP_Salary.overtime_threshold else 0
                # Overtime = min(Overtime, EMP_Salary.overtime_cap) # Cap has been moved to total (Monthly)

            else:
                posible_undertime = EMP_Salary.Regular_hours_cap - TotalWork
                Undertime = posible_undertime if posible_undertime >= EMP_Salary.undertime_threshold else 0

        Days.append({
            "Date": Date_constructor(Date),
            "Holiday": Holiday,
            "Total Work": day["TotalWork"],
            "Regular_hours": min(EMP_Salary.Regular_hours_cap, day["TotalWork"]),
            "Overtime": Overtime,
            "Undertime": Undertime,
            "off_Day_Overtime": off_day_overtime,
            "IsValid": True,
            "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]),
            "msg": "Finished"})
    return Days


# Teacher Replacement
def get_fingerprint_scanner(db: Session, user_id):
    try:
        user = db.query(dbm.Employees_form).filter_by(employees_pk_id=user_id, deleted=False).first()
        if not user:
            return 400, "Bad Request"
        return 200, db.query(dbm.Fingerprint_scanner_form).filter_by(user_ID=user.fingerprint_scanner_user_id, deleted=False).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_fingerprint_scanner(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: sch.Sort_Order = "desc"):
    try:
        return 200, record_order_by(db, dbm.Fingerprint_scanner_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def report_fingerprint_scanner(db: Session, salary, EnNo, start_date, end_date) -> tuple[int, str | dict]:
    Fingerprint_scanner_report = db.query(dbm.Fingerprint_scanner_form) \
        .filter(dbm.Fingerprint_scanner_form.Date.between(start_date, end_date)) \
        .filter_by(deleted=False, EnNo=EnNo).all()

    if not Fingerprint_scanner_report:
        return 400, f"Employee Has No fingerprint record from {start_date} to {end_date}"

    report_dicts = [{k: v for k, v in record.__dict__.items() if k != "_sa_instance_state"} for record in Fingerprint_scanner_report]
    final_result = {"Days": [], "total_Regular_hours": 0, "total_Overtime_hours": 0, "total_Undertime_hours": 0, "off_Day_Overtime": 0}

    # Split schedule and Fix schedule
    if salary.is_Fixed:
        final_result["Days"] = Fixed_schedule(salary, report_dicts)
    else:
        final_result["Days"] = Split_schedule(salary, report_dicts)

    final_result["total_Regular_hours"] = sum(day["Regular_hours"] for day in final_result["Days"])
    final_result["total_Overtime_hours"] = sum(day["Overtime"] for day in final_result["Days"])
    final_result["total_Undertime_hours"] = sum(day["Undertime"] for day in final_result["Days"])
    final_result["off_Day_Overtime"] = sum(day["off_Day_Overtime"] for day in final_result["Days"])
    return 200, final_result


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        OBJ = dbm.Fingerprint_scanner_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_bulk_fingerprint_scanner(db: Session, created_fk_by: uuid.UUID, file: UploadFile = File(...)):
    try:
        if not employee_exist(db, [created_fk_by]):
            return 400, "Bad Request"

        with open(f"./{file.filename}", "wb") as csv_file:
            csv_file.write(file.file.read())
        Data = pd.read_csv(f"./{file.filename}")

        start = datetime.combine(Fix_datetime(Data["DateTime"].min()), time())
        end = datetime.combine(Fix_datetime(Data["DateTime"].max()), time()) + timedelta(days=1)

        history = (
            db.query(dbm.Fingerprint_scanner_backup_form)
            .filter_by(deleted=False)
            .filter(dbm.Fingerprint_scanner_backup_form.DateTime.between(start, end))
            .all()
        )

        history = [(obj.__dict__["EnNo"], str(obj.__dict__["DateTime"])) for obj in history]

        Data = Data.to_dict(orient="records")

        OBJs, RES, ID = [], {}, {}

        if len(Data) == 0:
            return 400, "Empty File"

        for record in Data:
            del record["No"]
            record["In_Out"] = record.pop("In/Out")
            Signature = (record["EnNo"], record["DateTime"])
            logger.warning(f'{Signature}, {history}')
            if Signature in history:
                logger.warning(f'Exist: {Signature}')
                continue

            OBJs.append(dbm.Fingerprint_scanner_backup_form(created_fk_by=created_fk_by, **record))  # type: ignore[call-arg]
            record_time = record["DateTime"]
            EMP = record['Name']
            if EMP not in ID:
                ID[EMP] = record['EnNo']
            D, T = record_time.split(" ")
            if EMP not in RES:
                RES[EMP] = {}
            if D not in RES[EMP]:
                RES[EMP][D] = []
            RES[EMP][D].append(T)

        for EMP, Times in RES.items():
            for day, hour in Times.items():
                if len(hour) % 2:
                    hour.append(None)
                for H in range(0, len(hour), 2):
                    if hour[H] == hour[H + 1] or hour[H + 1] is None:
                        OBJs.append(dbm.Fingerprint_scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=0))  # type: ignore[call-arg]
                    else:
                        duration = 0 if hour[H] == hour[H + 1] else Fix_time(hour[H + 1]) - Fix_time(hour[H])
                        OBJs.append(dbm.Fingerprint_scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=duration.total_seconds() // 60))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "File added"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.Fingerprint_scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.Fingerprint_scanner_form).filter_by(teacher_tardy_reports_pk_id=Form.fingerprint_scanner_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
