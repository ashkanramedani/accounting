from datetime import timedelta, date, time, datetime
from typing import List, Dict

from db import models as dbm, Return_Exception
from lib import *
from lib.Date_Time import Debug

Day_Schema: dict


def calculate_duration(time_1: time | None, time_2: time | None):
    if time_1 is None or time_2 is None or time_1 == time_2:
        return 0
    return time_gap(time_1, time_2)


def Calculate_earning(salary_rate: dbm.Salary_Policy_form, **Total_activity):
    if not Total_activity:
        return {"Regular_earning": 0, "Overtime_earning": 0, "Undertime_earning": 0, "Off_Day_earning": 0}

    rates = {
        "Regular_earning": salary_rate.Base_salary * salary_rate.Regular_hours_factor * Total_activity["regular_work_time"],
        "Overtime_earning": salary_rate.Base_salary * salary_rate.overtime_factor * Total_activity["overtime"],
        "Undertime_earning": salary_rate.Base_salary * salary_rate.undertime_factor * Total_activity["undertime"],
        "Off_Day_earning": salary_rate.Base_salary * salary_rate.off_day_factor * Total_activity["off_Day_work_time"]
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
    try:
        Date_obj = Fix_date(Date_obj)
        if Date_obj.year > 2000:
            M_Date = Date_obj
            P_Date = to_persian(Date_obj.year, Date_obj.month, Date_obj.day, return_obj=False)
        else:
            M_Date = to_international(Date_obj.year, Date_obj.month, Date_obj.day, return_obj=False)
            P_Date = Date_obj
        return f'{M_Date}  {P_Date}'
    except Exception as e:
        return f"Date_constructor: {e}"


def Create_Day_Schema(Date: str | date | datetime, Activities: Dict, message="Created") -> Dict:
    return {
        "Date": Date_constructor(Date),
        "Holiday": is_off_day(Fix_date(Date)),
        "Accrued_Holiday": False,
        "IsValid": True,
        "present_time": 0,
        "Regular_hours": 0,
        "Overtime": 0,
        "Undertime": 0,
        "off_Day_Overtime": 0,
        "delay": 0,
        "haste": 0,
        "attendance_points": 0,
        "remote": Activities["remote"].get(str(Date), 0),
        "vacation_leave": Activities["vacation_leave"].get(str(Date), 0),
        "medical_leave": Activities["medical_leave"].get(str(Date), 0),
        "business_trip": Activities["business_trip"].get(str(Date), 0),
        "EnterExit": [],
        "msg": message}


def preprocess_report(report, Activities: Dict):
    """
    This Function Preprocesses the Report on each Enter/Exit.
        - group the enter and exit by date
        - calculates the time gap (total present time)
        - add missing days to calender
    """
    Days = {}
    for i, record in enumerate(report):
        Key = str(record.Date)

        if Key not in Days:
            Days[Key] = Create_Day_Schema(record.Date, Activities)

        if not record.Enter or not record.Exit:
            Days[Key]["IsValid"] = False
            Days[Key]["msg"] = "invalid Enter/exit time"

        else:
            Days[Key]["present_time"] += time_gap(record.Enter, record.Exit)

        Days[Key]["EnterExit"].extend([record.Enter, record.Exit])
        for Date in add_missing_day(report[i: i + 2]):
            Days[Date] = Create_Day_Schema(record.Date, Activities, message="Not Present")
    return Days


def add_missing_day(seq: list) -> List[str]:
    if len(seq) < 2:
        return []
    missing_day = []
    currentDay: date = seq[0].Date
    while currentDay < seq[1].Date:
        currentDay += timedelta(days=1)
        missing_day.append(str(currentDay))
    return missing_day[:-1]


def Fixed_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> List[Dict]:
    Days = []
    
    for Date, Day_OBJ in preprocess_Days.items():
        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Days.append(Day_OBJ)
            continue

        # present on Holiday
        if Day_OBJ["Holiday"]:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = Day_OBJ["present_time"]
                Day_OBJ["Regular_hours"] = max(0, EMP_Salary.Regular_hours_cap - Day_OBJ["present_time"])


        # Not Present on working day
        elif not Day_OBJ["EnterExit"]:
            Day_OBJ["Undertime"] = EMP_Salary.Regular_hours_cap

        # Present on working day
        else:
            EnterExit = Day_OBJ["EnterExit"]
            EnterExit.sort()

            first_enter, last_exit = max(EnterExit[0], EMP_Salary.day_starting_time), EnterExit[-1]

            # UnderTime
            tmp_undertime = time_gap(EMP_Salary.day_starting_time, first_enter)
            if tmp_undertime > EMP_Salary.undertime_threshold:
                Day_OBJ["Undertime"] = tmp_undertime
                Day_OBJ["delay"] = tmp_undertime

            if last_exit < EMP_Salary.day_ending_time:
                tmp_undertime = time_gap(last_exit, EMP_Salary.day_ending_time)
                if tmp_undertime > EMP_Salary.undertime_threshold:
                    Day_OBJ["Undertime"] += tmp_undertime
                    Day_OBJ["haste"] = tmp_undertime
            else:
                tmp_overtime = time_gap(EMP_Salary.day_ending_time, last_exit)
                if tmp_overtime > EMP_Salary.overtime_threshold:
                    Day_OBJ["Overtime"] = tmp_overtime

            # check if more than one Enter and Exit is in day
            EnterExit = EnterExit[1:-1]
            if EnterExit:
                for Enter, Exit in zip(EnterExit[1:2], EnterExit[:2]):
                    Day_OBJ["Undertime"] += time_gap(Enter, Exit)

            Day_OBJ["Regular_hours"] = min(Day_OBJ["present_time"] - Day_OBJ["Overtime"], EMP_Salary.Regular_hours_cap)

        Day_OBJ["EnterExit"] = ' '.join([str(t) for t in Day_OBJ.pop("EnterExit", [])])
        Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
    return Days


def Split_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> List[Dict]:
    Days = []

    for Date, Day_OBJ in preprocess_Days.items():
        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Days.append(Day_OBJ)
            continue

        if Day_OBJ["Holiday"]:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = Day_OBJ["present_time"]
                Day_OBJ["Regular_hours"] = max(0, EMP_Salary.Regular_hours_cap - Day_OBJ["present_time"])
        else:
            if Day_OBJ["present_time"] >= EMP_Salary.Regular_hours_cap:
                possible_Overtime = Day_OBJ["present_time"] - EMP_Salary.Regular_hours_cap
                Day_OBJ["Overtime"] = possible_Overtime if possible_Overtime >= EMP_Salary.overtime_threshold else 0
            else:
                possible_undertime = EMP_Salary.Regular_hours_cap - Day_OBJ["present_time"]
                Day_OBJ["Undertime"] = possible_undertime if possible_undertime >= EMP_Salary.undertime_threshold else 0
            Day_OBJ["Regular_hours"] = min(EMP_Salary.Regular_hours_cap, Day_OBJ["present_time"])

            Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
    return Days


def Hourly_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> List[Dict]:
    Days = []
    for Date, Day_OBJ in preprocess_Days.items():
        if Day_OBJ["Accrued_Holiday"]:
            Day_OBJ["msg"] = "Accrued_Holiday"
            Days.append(Day_OBJ)
            continue

        if not Day_OBJ["IsValid"]:
            Days.append(Day_OBJ)
            continue

        if Day_OBJ["Holiday"]:
            if EMP_Salary.off_day_permission:
                Day_OBJ["off_Day_Overtime"] = Day_OBJ["present_time"]
        else:  # NC: 005
            if EMP_Salary.Regular_hours_cap > Day_OBJ["present_time"]:
                Day_OBJ["attendance_points"] -= 1
            Day_OBJ["Regular_hours"] = min(EMP_Salary.Regular_hours_cap, Day_OBJ["present_time"])

        Day_OBJ["msg"] = "Finished"
        Days.append(Day_OBJ)
    return Days


def generate_daily_report(Salary_Policy: dbm.Salary_Policy_form, Fingerprint_scanner_report: List[dbm.Fingerprint_Scanner_form], Activities: Dict):
    """
    Generate the daily report Base on Employee fingerprint scanner report
    """
    try:
        
        final_result = {}
        report_dicts = preprocess_report(Fingerprint_scanner_report, Activities)
        
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
        return Return_Exception(Error=e)
