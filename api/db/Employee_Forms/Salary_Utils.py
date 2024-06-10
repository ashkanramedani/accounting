from datetime import timedelta, date, time, datetime
from typing import List, Tuple, Dict

import db.models as dbm
from lib import *
from ..Extra import *

Day_Schema: dict


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


def Sum_of_Activity(salary_rate, Day_activity: List) -> Dict[str, int]:
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
    This Function Preprocesses the Report on each Enter/Exit.
        - calculates the time gap
        - add missing days to calender
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
                    Accrued_Holiday: bool
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
        # present on Holiday
        if Holiday:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = day["present_time"]

        # Not Present on working day
        elif not day["EnterExit"]:
            Day_OBJ["Undertime"] = EMP_Salary.Regular_hours_cap

        # Present on working day
        else:
            EnterExit = day["EnterExit"]
            EnterExit.sort()

            first_enter, last_exit = max(EnterExit[0], EMP_Salary.day_starting_time), EnterExit[-1]

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
                    Accrued_Holiday: bool
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
                    Accrued_Holiday: bool
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


def generate_daily_report(Salary_Policy: dbm.Salary_Policy_form, Fingerprint_scanner_report: List[dbm.Fingerprint_Scanner_form]):
    """
    Generate the daily report Base on Employee fingerprint scanner report
    """
    try:
        final_result = {}
        report_dicts = preprocess_report([{k: v for k, v in record.__dict__.items() if k != "_sa_instance_state"} for record in Fingerprint_scanner_report])

        # Split schedule and Fix schedule
        if Salary_Policy.Salary_Type == "Fixed":
            final_result["Days"]: List[dict] = Fixed_schedule(Salary_Policy, report_dicts)
        elif Salary_Policy.Salary_Type == "Split":
            final_result["Days"]: List[dict] = Split_schedule(Salary_Policy, report_dicts)
        elif Salary_Policy.Salary_Type == "Hourly":
            final_result["Days"]: List[dict] = Hourly_schedule(Salary_Policy, report_dicts)
        else:
            return 400, "Invalid Salary Type"

        Total_Activity = Sum_of_Activity(Salary_Policy, final_result["Days"])
        final_result |= Total_Activity
        final_result |= Calculate_earning(Salary_Policy, **Total_Activity)
        return 200, final_result
    except Exception as e:
        return 500, f'{e.__class__.__name__}: {e.args}'
