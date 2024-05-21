import json
import pickle
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


def calculate_duration(time_1: time | None, time_2: time | None):
    if time_1 is None or time_2 is None or time_1 == time_2:
        return 0
    return time_gap(time_1, time_2)


def Calculate_earning(salary_rate: dbm.Salary_Policy_form, **Total_activity):
    if not Total_activity:
        return {"Regular_earning": 0, "Overtime_earning": 0, "Undertime_earning": 0, "Off_Day_earning": 0}

    rates = {
        "Regular_earning": salary_rate.Base_salary * salary_rate.Regular_hours_factor * (Total_activity["regular_work_time"] / 60),
        "Overtime_earning": salary_rate.Base_salary * salary_rate.overtime_factor * (Total_activity["overtime"] / 60),
        "Undertime_earning": salary_rate.Base_salary * salary_rate.undertime_factor * (Total_activity["undertime"] / 60),
        "Off_Day_earning": salary_rate.Base_salary * salary_rate.off_day_factor * (Total_activity["off_Day_work_time"] / 60)
    }
    return rates


def Sum_of_Activity(salary_rate, Day_activity: List):
    if not Day_activity:
        return {"present_time": 0, "regular_work_time": 0, "overtime": 0, "undertime": 0, "off_Day_work_time": 0}

    rates = {
        "present_time": sum(day["present_time"] for day in Day_activity),
        "regular_work_time": sum(day["Regular_hours"] for day in Day_activity),
        "overtime": min(sum(day["Overtime"] for day in Day_activity), salary_rate.overtime_cap),
        "undertime": sum(day["Undertime"] for day in Day_activity),
        "off_Day_work_time": min(sum(day["off_Day_Overtime"] for day in Day_activity), salary_rate.off_day_cap)
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


def Create_Day_Schema(Date: str | date | datetime, day: dict, Holiday: bool) -> Dict:
    return {
        "Date": Date_constructor(Date),
        "Holiday": Holiday,
        "Accrued_Holiday": False,
        "present_time": 0,
        "Regular_hours": 0,
        "Overtime": 0,
        "Undertime": 0,
        "off_Day_Overtime": 0,
        "IsValid": day["IsValid"],
        "EnterExit": ' '.join([str(t) for t in day["EnterExit"]]),
        "msg": "Created"}


def preprocess_report(report):
    """
    This Function Preprocesses the Report. on each Enter/Exit time it calculates the time gap and add missing days to calender
    """
    Days = {}
    for i, record in enumerate(report):
        Key = str(record["Date"])

        if Key not in Days:
            Days[Key] = {"present_time": 0, "EnterExit": [], "IsValid": True, "msg": "Normal"}

        if not record["Enter"] or not record["Exit"]:
            Days[Key]["IsValid"] = False
            Days[Key]["msg"] = "invalid Enter/exit time"

        else:
            Days[Key]["present_time"] += time_gap(record["Enter"], record["Exit"])
        Days[Key]["EnterExit"].extend([record["Enter"], record["Exit"]])

        for Date, Date_data in add_missing_day(report[i: i + 2]):
            Days[Date] = Date_data
    return Days


def add_missing_day(seq: list) -> List[Tuple]:
    if len(seq) < 2:
        return []
    missing_day = []
    currentDay: date = seq[0]["Date"]
    while currentDay < seq[1]["Date"]:
        currentDay += timedelta(days=1)
        missing_day.append((str(currentDay), {"present_time": 0, "EnterExit": [], "IsValid": True, "msg": "Not Present"}))
    return missing_day[:-1]


def Fixed_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> List[Dict]:
    """
    :return: List[{
                    Date: str
                    Holiday: bool
                    present_time: int
                    Regular_hours: int
                    Overtime: int
                    Undertime: int
                    off_Day_Overtime: int
                    IsValid: bool
                    EnterExit: str
                    msg: str}]
    """
    Days = []
    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))
        Day_OBJ = Create_Day_Schema(Date, day, Holiday)

        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Day_OBJ["msg"] = day["msg"]
            Days.append(Day_OBJ)
            continue

        Day_OBJ["present_time"] = day["present_time"]
        if Holiday:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = day["present_time"]

        elif not day["EnterExit"]:
            Day_OBJ["Undertime"] = EMP_Salary.Regular_hours_cap

        else:
            EnterExit = day["EnterExit"]
            EnterExit.sort()
            first_enter = max(EnterExit[0], EMP_Salary.day_starting_time)
            res = {
                "first_enter": first_enter,
                "day['EnterExit']": day["EnterExit"],
                "min(day['EnterExit'])": min(day["EnterExit"]),
                "EMP_Salary.day_starting_time": EMP_Salary.day_starting_time
            }

            # logger.warning(json.dumps(res, indent=4, cls=JSONEncoder))
            last_exit = EnterExit[-1]
            # UnderTime
            tmp_undertime = time_gap(EMP_Salary.day_starting_time, first_enter)
            if tmp_undertime > EMP_Salary.undertime_threshold:
                Day_OBJ["Undertime"] = tmp_undertime

            if last_exit < EMP_Salary.day_ending_time:
                tmp_undertime = time_gap(last_exit, EMP_Salary.day_ending_time)
                if tmp_undertime > EMP_Salary.undertime_threshold:
                    Day_OBJ["Undertime"] += tmp_undertime
            else:
                tmp_overtime = time_gap(EMP_Salary.day_ending_time, last_exit)
                if tmp_overtime > EMP_Salary.overtime_threshold:
                    Day_OBJ["Overtime"] = tmp_overtime

            # check if more than one Enter and Exit is in day
            if len(EnterExit) > 2:
                for Enter, Exit in zip(EnterExit[2::2], EnterExit[1:-1:2]):
                    day["Undertime"] += time_gap(Enter, Exit)

            Day_OBJ["Regular_hours"] = min(day["present_time"] - Day_OBJ["Overtime"], EMP_Salary.Regular_hours_cap)

        Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
    return Days

def Split_schedule(EMP_Salary, preprocess_Days) -> List[Dict]:
    """
    :return: List[{
                    Date: str
                    Holiday: bool
                    present_time: int
                    Regular_hours: int
                    Overtime: int
                    Undertime: int
                    off_Day_Overtime: int
                    IsValid: bool
                    EnterExit: str
                    msg: str}]
    """
    Days = []

    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))
        Day_OBJ = Create_Day_Schema(Date, day, Holiday)

        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Day_OBJ["msg"] = day["msg"]
            Days.append(Day_OBJ)
            continue

        Day_OBJ["present_time"] = day["present_time"]
        if Holiday:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = day["present_time"]
        else:
            if Day_OBJ["present_time"] >= EMP_Salary.Regular_hours_cap:
                posible_Overtime = Day_OBJ["present_time"] - EMP_Salary.Regular_hours_cap
                Day_OBJ["Overtime"] = posible_Overtime if posible_Overtime >= EMP_Salary.overtime_threshold else 0
            else:
                posible_undertime = EMP_Salary.Regular_hours_cap - Day_OBJ["present_time"]
                Day_OBJ["Undertime"] = posible_undertime if posible_undertime >= EMP_Salary.undertime_threshold else 0
            Day_OBJ["Regular_hours"] = min(EMP_Salary.Regular_hours_cap, day["present_time"])

            Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
    return Days

def Hourly_schedule(EMP_Salary, preprocess_Days) -> List[Dict]:
    """
    :return: List[{
                    Date: str
                    Holiday: bool
                    present_time: int
                    Regular_hours: int
                    Overtime: int
                    Undertime: int
                    off_Day_Overtime: int
                    IsValid: bool
                    EnterExit: str
                    msg: str}]
    """
    Days = []
    for Date, day in preprocess_Days.items():
        Holiday = is_off_day(Fix_date(Date))
        Day_OBJ = Create_Day_Schema(Date, day, Holiday)

        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Day_OBJ["msg"] = day["msg"]
            Days.append(Day_OBJ)
            continue

        Day_OBJ["present_time"] = day["present_time"]
        if Holiday:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = day["present_time"]
        else:
            Day_OBJ["Regular_hours"] = min(EMP_Salary.Regular_hours_cap, day["present_time"])

        Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
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


def report_fingerprint_scanner(db: Session, Salary_Policy, EnNo, start_date, end_date) -> Dict | str:
    Fingerprint_scanner_report = db.query(dbm.Fingerprint_Scanner_form) \
        .filter(dbm.Fingerprint_Scanner_form.Date.between(start_date, end_date)) \
        .filter_by(deleted=False, EnNo=EnNo).all()

    if not Fingerprint_scanner_report:
        return f"Employee Has No fingerprint record from {start_date} to {end_date}"

    report_dicts = [{k: v for k, v in record.__dict__.items() if k != "_sa_instance_state"} for record in Fingerprint_scanner_report]
    final_result = {}

    report2 = {}
    for i, record in enumerate(report_dicts):
        report2[i] = {k: str(v) for k, v in record.items() if k in ["Date", "Enter", "Exit", "EnNo", "duration"]}
    report_dicts = preprocess_report(report_dicts)

    # Split schedule and Fix schedule
    if Salary_Policy.is_Fixed:
        final_result["Days"]: List[dict] = Fixed_schedule(Salary_Policy, report_dicts)
    else:
        final_result["Days"]: List[dict] = Split_schedule(Salary_Policy, report_dicts)

    Total_Activity = Sum_of_Activity(Salary_Policy, final_result["Days"])
    final_result |= Total_Activity
    final_result |= Calculate_earning(Salary_Policy, **Total_Activity)
    return final_result


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        if data["Enter"]:
            data["Enter"] = Fix_time(data["Enter"]).replace(second=0)
        if data["Exit"]:
            data["Exit"] = Fix_time(data["Exit"]).replace(second=0)
        OBJ = dbm.Fingerprint_Scanner_form(**data)  # type: ignore[call-arg]

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

        Data = pd.read_csv(file.file)
        if "No" in Data.columns:
            Data = Data.drop("No", axis=1)

        try:
            Data["DateTime"] = pd.to_datetime(Data["DateTime"], errors='coerce').dt.floor('min')
            Data = Data.sort_values(by="DateTime").drop_duplicates()
            Data.rename(columns={"In/Out": "In_Out"}, inplace=True)
        except pd.errors.ParserError:
            return 400, f"Error parsing the CSV."

        start = datetime.combine(Data.iloc[0]["DateTime"], time())
        end = datetime.combine(Data.iloc[-1]["DateTime"] + pd.Timedelta(days=1), time())
        history = (
            db.query(dbm.Fingerprint_Scanner_backup_form)
            .filter_by(deleted=False)
            .filter(dbm.Fingerprint_Scanner_backup_form.DateTime.between(start, end))
            .all()
        )

        history = [f'{obj.__dict__["EnNo"]}_{str(obj.__dict__["DateTime"])}' for obj in history]

        Data = Data.to_dict(orient="records")

        OBJs, RES, ID = [], {}, {}

        if len(Data) == 0:
            logger.warning('400, "Empty File"')
            return 400, "Empty File"

        for record in Data:
            Signature = f'{record["EnNo"]}_{record["DateTime"]}'
            if Signature in history:
                continue

            OBJs.append(dbm.Fingerprint_Scanner_backup_form(created_fk_by=created_fk_by, **record))  # type: ignore[call-arg]
            record_time = record["DateTime"]
            EMP = record['Name']
            if EMP not in ID:
                ID[EMP] = record['EnNo']
            D, T = record_time.date(), record_time.time()
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
                    duration = calculate_duration(hour[H], hour[H + 1])
                    hour[H] = Fix_time(hour[H]) if hour[H] else None
                    hour[H + 1] = Fix_time(hour[H + 1]) if hour[H + 1] else None
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
