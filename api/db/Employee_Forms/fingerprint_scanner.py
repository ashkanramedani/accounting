import uuid
from datetime import timedelta, date, time, datetime
from typing import List, Tuple, Dict

import pandas as pd
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import *

from ..Extra import *


def Calculate_earning(salary_rate: dbm.Salary_Policy_form, **Total_activity):
    if not Total_activity:
        return {"Total": 0, "Regular": 0, "Overtime": 0, "Undertime": 0, "Off_Day": 0}

    rates = {
        "Regular": salary_rate.Regular_hours_factor * Total_activity["Regular"],
        "Overtime": salary_rate.overtime_factor * Total_activity["Overtime"],
        "Undertime": salary_rate.undertime_factor * Total_activity["Undertime"],
        "Off_Day": salary_rate.off_day_factor * Total_activity["Off_Day"]
    }
    rates["Total"] = sum(rates.values())
    return rates


"""
Regular_hours_factor
overtime_factor
undertime_factor
off_day_factor
"""


def Sum_of_Activity(salary_rate, Day_activity: List):
    if not Day_activity:
        return {"Total": 0, "Regular": 0, "Overtime": 0, "Undertime": 0, "Off_Day": 0}

    rates = {
        "Total": sum(day["Total_Work"] for day in Day_activity),
        "Regular": sum(day["Regular_hours"] for day in Day_activity),
        "Overtime": min(sum(day["Overtime"] for day in Day_activity), salary_rate.overtime_cap),
        "Undertime": sum(day["Undertime"] for day in Day_activity),
        "Off_Day": min(sum(day["off_Day_Overtime"] for day in Day_activity), salary_rate.off_day_cap)
    }
    return rates


def Date_constructor(Date_obj: str | date | datetime):
    Date_obj = Fix_date(Date_obj)
    if Date_obj.year > 2000:
        M_Date = Date_obj
        P_Date = to_persian(Date_obj.year, Date_obj.month, Date_obj.day)
    else:
        M_Date = to_international(Date_obj.year, Date_obj.month, Date_obj.day)
        P_Date = Date_obj
    return f'{M_Date}  {P_Date}'


def add_missing_day(seq: list) -> List[Tuple]:
    if len(seq) < 2:
        return []
    missing_day = []
    currentDay: date = seq[0]["Date"]
    while currentDay < seq[1]["Date"]:
        currentDay += timedelta(days=1)
        missing_day.append((str(currentDay), {"Total_Work": 0, "EnterExit": [], "IsValid": True, "msg": "Not Present"}))
    return missing_day


def preprocess_report(report):
    preprocess_Days = {}
    for i in range(len(report) - 1):
        Key = str(report[i]["Date"])
        if report[i]["Enter"] is None or report[i]["Exit"] is None:
            preprocess_Days[Key] = {"Total_Work": 0, "EnterExit": [report[i]["Enter"], report[i]["Exit"]], "IsValid": False, "msg": 'invalid Enter/exit time'}
            continue
        if report[i]["Date"] not in preprocess_Days:
            preprocess_Days[Key] = {"Total_Work": 0, "EnterExit": [], "IsValid": True, "msg": "Processed"}

        preprocess_Days[Key]["Total_Work"] += time_gap(report[i]["Enter"], report[i]["Exit"])
        preprocess_Days[Key]["EnterExit"].append(report[i]["Enter"])
        preprocess_Days[Key]["EnterExit"].append(report[i]["Exit"])

        for Date, Date_data in add_missing_day(report[i: i + 2]):
            preprocess_Days[Date] = Date_data

    return preprocess_Days


def Fixed_schedule(EMP_Salary: dbm.Salary_Policy_form, report) -> List[Dict]:
    """
    :return: List[{
                    Date: str
                    Holiday: bool
                    Total_Work: int
                    Regular_hours: int
                    Overtime: int
                    Undertime: int
                    off_Day_Overtime: int
                    IsValid: bool
                    EnterExit: str
                    msg: str
                }]
    """
    preprocess_Days = preprocess_report(report)
    Days = []
    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))

        Overtime, Undertime, Regular_hours, off_day_overtime, Total_Work = 0, 0, 0, 0, 0
        if not day["IsValid"]:
            Days.append({"Date": Date_constructor(Date), "Holiday": Holiday, "Total_Work": 0, "Regular_hours": 0, "Overtime": 0, "Undertime": 0, "off_Day_Overtime": 0, "IsValid": False, "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]), "msg": day["msg"]})
            continue

        if Holiday:
            if EMP_Salary.off_day_permission:
                off_day_overtime = day["Total_Work"]

        elif not day["EnterExit"]:
            Overtime = 0
            Undertime = EMP_Salary.Regular_hours_cap

        else:
            first_enter: time = max(min(day["EnterExit"]), EMP_Salary.day_starting_time)  # type: ignore
            last_exit: time = max(day["EnterExit"])  # type: ignore
            # UnderTime
            tmp_undertime = time_gap(EMP_Salary.day_starting_time, first_enter)
            Undertime = tmp_undertime if tmp_undertime > EMP_Salary.undertime_threshold else 0

            if last_exit < EMP_Salary.day_ending_time:
                tmp_undertime = time_gap(last_exit, EMP_Salary.day_ending_time)
                Undertime += tmp_undertime if tmp_undertime > EMP_Salary.undertime_threshold else 0
            else:
                tmp_overtime = time_gap(EMP_Salary.day_ending_time, last_exit)
                Overtime = tmp_overtime if tmp_overtime > EMP_Salary.overtime_threshold else 0

            EnterExit = day["EnterExit"]
            EnterExit.sort()
            enters = EnterExit[2::2]
            exits = EnterExit[1:-1:2]
            # check if more than one Enter and Exit is in day
            if len(EnterExit) != 2:
                for Enter, Exit in zip(enters, exits):
                    day["Undertime"] += time_gap(Enter, Exit)

        Days.append({"Date": Date_constructor(Date), "Holiday": Holiday, "Total_Work": day["Total_Work"], "Regular_hours": min(day["Total_Work"] - Overtime, EMP_Salary.Regular_hours_cap) if not off_day_overtime else 0, "Overtime": Overtime, "Undertime": Undertime, "off_Day_Overtime": off_day_overtime, "IsValid": True, "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]), "msg": "Finished"})
    return Days


def Split_schedule(EMP_Salary, reports) -> List[Dict]:
    """
    :return: List[{
                    Date: str
                    Holiday: bool
                    Total_Work: int
                    Regular_hours: int
                    Overtime: int
                    Undertime: int
                    off_Day_Overtime: int
                    IsValid: bool
                    EnterExit: str
                    msg: str
                }]
    """
    preprocess_Days = preprocess_report(reports)
    Days = []

    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))
        Overtime, Undertime, Regular_hours, off_day_overtime = 0, 0, 0, 0
        if not day["IsValid"]:
            Days.append({
                "Date": Date_constructor(Date),
                "Holiday": Holiday,
                "Total_Work": 0,
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
                off_day_overtime = day["Total_Work"]
        else:
            Total_Work = day["Total_Work"]

            if Total_Work >= EMP_Salary.Regular_hours_cap:
                posible_Overtime = Total_Work - EMP_Salary.Regular_hours_cap
                Overtime = posible_Overtime if posible_Overtime >= EMP_Salary.overtime_threshold else 0

            else:
                posible_undertime = EMP_Salary.Regular_hours_cap - Total_Work
                Undertime = posible_undertime if posible_undertime >= EMP_Salary.undertime_threshold else 0

        Days.append({
            "Date": Date_constructor(Date),
            "Holiday": Holiday,
            "Total_Work": day["Total_Work"],
            "Regular_hours": min(EMP_Salary.Regular_hours_cap, day["Total_Work"]),
            "Overtime": Overtime,
            "Undertime": Undertime,
            "off_Day_Overtime": off_day_overtime,
            "IsValid": True,
            "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]),
            "msg": "Finished"})
    return Days


# Teacher Replacement
def get_fingerprint_scanner(db: Session, form_id):
    try:
        return 200, db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_fingerprint_scanner(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: sch.Sort_Order = "desc"):
    try:
        return 200, record_order_by(db, dbm.Fingerprint_Scanner_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_fingerprint_scanner(db: Session, Salary_Policy, EnNo, start_date, end_date) -> tuple[int, str | dict]:
    Fingerprint_scanner_report = db.query(dbm.Fingerprint_Scanner_form) \
        .filter(dbm.Fingerprint_Scanner_form.Date.between(start_date, end_date)) \
        .filter_by(deleted=False, EnNo=EnNo).all()

    if not Fingerprint_scanner_report:
        return 400, f"Employee Has No fingerprint record from {start_date} to {end_date}"

    report_dicts = [{k: v for k, v in record.__dict__.items() if k != "_sa_instance_state"} for record in Fingerprint_scanner_report]
    final_result = {}
    # Split schedule and Fix schedule
    if Salary_Policy.is_Fixed:
        final_result["Days"]: List[dict] = Fixed_schedule(Salary_Policy, report_dicts)
    else:
        final_result["Days"]: List[dict] = Split_schedule(Salary_Policy, report_dicts)

    final_result["Total_Activity"] = Sum_of_Activity(Salary_Policy, final_result["Days"])
    final_result["Earning"] = Calculate_earning(Salary_Policy, **final_result["Total_Activity"])
    return 200, final_result


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        OBJ = dbm.Fingerprint_Scanner_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_bulk_fingerprint_scanner(db: Session, created_fk_by: uuid.UUID, file: UploadFile = File(...)):
    try:
        if not employee_exist(db, [created_fk_by]):
            return 400, "Bad Request: Employee Does Not Exist"

        logger.warning(f'{type(file)} {file.filename}')
        Data = pd.read_csv(file.file)
        # if isinstance(file, UploadFile):
        #     pass
        # else:
        #     logger.warning('400, "File is Not Acceptable"')
        #     return 400, "File is Not Acceptable"

        start = datetime.combine(Fix_datetime(Data["DateTime"].min()), time())
        end = datetime.combine(Fix_datetime(Data["DateTime"].max()), time()) + timedelta(days=1)

        history = (
            db.query(dbm.Fingerprint_Scanner_backup_form)
            .filter_by(deleted=False)
            .filter(dbm.Fingerprint_Scanner_backup_form.DateTime.between(start, end))
            .all()
        )

        history = [(obj.__dict__["EnNo"], str(obj.__dict__["DateTime"])) for obj in history]

        Data = Data.to_dict(orient="records")

        OBJs, RES, ID = [], {}, {}

        if len(Data) == 0:
            logger.warning('400, "Empty File"')
            return 400, "Empty File"

        for record in Data:
            del record["No"]
            record["In_Out"] = record.pop("In/Out")
            Signature = (record["EnNo"], record["DateTime"])
            if Signature in history:
                continue

            OBJs.append(dbm.Fingerprint_Scanner_backup_form(created_fk_by=created_fk_by, **record))  # type: ignore[call-arg]
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
                        OBJs.append(dbm.Fingerprint_Scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=0))  # type: ignore[call-arg]
                    else:
                        duration = 0 if hour[H] == hour[H + 1] else time_gap(Fix_time(hour[H]), Fix_time(hour[H + 1]))
                        OBJs.append(dbm.Fingerprint_Scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=duration))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "File added"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=Form.fingerprint_scanner_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()

        s, e = data["Enter"], data["Exit"]
        data["duration"] = 0 if s == e else time_gap(Fix_time(s), Fix_time(s))

        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


"""
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
            db.query(dbm.Fingerprint_Scanner_backup_form)
            .filter_by(deleted=False)
            .filter(dbm.Fingerprint_Scanner_backup_form.DateTime.between(start, end))
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
            if Signature in history:
                continue

            OBJs.append(dbm.Fingerprint_Scanner_backup_form(created_fk_by=created_fk_by, **record))  # type: ignore[call-arg]
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
                        OBJs.append(dbm.Fingerprint_Scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=0))  # type: ignore[call-arg]
                    else:
                        duration = 0 if hour[H] == hour[H + 1] else time_gap(Fix_time(hour[H]), Fix_time(hour[H + 1]))
                        OBJs.append(dbm.Fingerprint_Scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=duration))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "File added"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


"""

"""
Expected type 'list[DaySchadule]', 
got 'list[dict[str, str | list | int | bool] | dict[str, str | list | int | bool | Any]]' instead """