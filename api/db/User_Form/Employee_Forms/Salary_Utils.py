from datetime import timedelta, date, time, datetime
from typing import List, Dict, Literal, Tuple

from db import Return_Exception
import models as dbm
from lib import *
from lib import DEV_io

Day_Schema: dict
INF: int = 50000


def calculate_duration(time_1: time | None, time_2: time | None):
    if time_1 is None or time_2 is None or time_1 == time_2:
        return 0
    return time_gap(time_1, time_2)


@DEV_io()
def Calculate_income(salary_rate: dbm.Salary_Policy_form, Total_activity: Dict, Total_Holiday: int):
    Base_Salary = salary_rate.Base_salary

    Salary_on_Holiday = Total_Holiday * salary_rate.Regular_hours_cap
    total_off_day = Total_activity["Off_Day"] if salary_rate.off_day_permission else 0

    earning: Dict[str, float] = {
        "Regular_earning": salary_rate.Regular_hours_factor * Total_activity["Regular_hours"],
        "Overtime_earning": salary_rate.overtime_factor * Total_activity["Overtime"] if salary_rate.overtime_permission else 0,
        "Off_Day_earning": (min(0, Salary_on_Holiday - total_off_day) * salary_rate.Regular_hours_factor) + (total_off_day * salary_rate.off_day_factor),
        "remote_earning": salary_rate.remote_factor * Total_activity["remote"] if salary_rate.remote_permission else 0,
        "business_trip_earning": salary_rate.business_trip_factor * Total_activity["business_trip"] if salary_rate.business_trip_permission else 0,
        "vacation_leave_earning": salary_rate.vacation_leave_factor * (salary_rate.vacation_leave_cap - Total_activity["vacation_leave"]),
        "medical_leave_earning": salary_rate.medical_leave_factor * (min(0, salary_rate.medical_leave_cap - Total_activity["medical_leave"]))
    }

    earning = {k: v * Base_Salary for k, v in earning.items()}
    earning |= {"rewards_earning": 0, "Fix_pay": salary_rate.Fix_pay}

    # Should be all Positive
    deduction = {
        "Undertime_deductions": Base_Salary * salary_rate.undertime_factor * Total_activity["Undertime"],
        "insurance_deductions": 0,
        "tax_deductions": 0,
        "punishment_deductions": 0
    }

    total_earning = sum(earning.values())
    total_deduction = abs(sum(deduction.values()))
    return {**earning, **deduction,
            "total_earning": total_earning,
            "total_deduction": total_deduction,
            "total_income": total_earning - total_deduction}


@DEV_io()
def Sum_of_Activity(salary_rate: dbm.Salary_Policy_form, Day_activity: List[Dict]) -> Dict[str, int]:
    caps = {
        "Overtime": salary_rate.overtime_cap,
        "Off_Day": salary_rate.off_day_cap,
        "remote": salary_rate.remote_cap,
        "vacation_leave": salary_rate.vacation_leave_cap,
        "medical_leave": salary_rate.medical_leave_cap,
        "business_trip": salary_rate.business_trip_cap}

    rates = {
        key: min(sum(day[key] for day in Day_activity), caps.get(key, INF))
        for key in ["present_time", "Regular_hours", "Overtime", "Undertime", "Off_Day", "delay", "haste", "attendance_points", "remote", "vacation_leave", "medical_leave", "business_trip"]
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
    activities = {field: Activities[field].get(str(Date), 0) for field in ["remote", "vacation_leave", "medical_leave", "business_trip"]}
    return {
        "Date": Date_constructor(Date),
        "Holiday": is_off_day(Fix_date(Date)),
        "Accrued_Holiday": False,
        "IsValid": True,
        "present_time": 0,
        "Regular_hours": 0,
        "Overtime": 0,
        "Undertime": 0,
        "Off_Day": 0,
        "delay": 0,
        "haste": 0,
        "attendance_points": 0,
        "EnterExit": [],
        "msg": message,
        **activities}


@DEV_io()
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
            Days[Key] = Create_Day_Schema(Key, Activities)

        if not record.Enter or not record.Exit:
            Days[Key]["IsValid"] = False
            Days[Key]["msg"] = "invalid Enter/exit time"

        else:
            Days[Key]["present_time"] += time_gap(record.Enter, record.Exit)

        Days[Key]["EnterExit"].extend([record.Enter, record.Exit])
        missing_seq = report[i: i + 2]
        if len(missing_seq) == 2:
            start_date = missing_seq[0].Date
            for Date in [str(start_date + timedelta(days=i)) for i in range(1, (missing_seq[1].Date - start_date).days)]:
                Days[Date] = Create_Day_Schema(Date, Activities, message="Not Present")
    return Days


def Accrued_Holiday(Day):
    Day["msg"] = "Accrued_Holiday"
    return Day

def finalize(Day: Dict) -> Dict:
    Day["Undertime"] = max(0, Day["Undertime"] - sum(Day[field] for field in ["remote", "vacation_leave", "medical_leave", "business_trip"]))
    Day["EnterExit"] = ' '.join([str(t) for t in Day.pop("EnterExit", [])])
    Day["msg"] = "Finished"
    return Day

@DEV_io()
def Fixed_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days: Dict[str, Dict]) -> Tuple[List[Dict], int]:
    Total_Holiday = 0
    Days = []

    for Date, Day_OBJ in preprocess_Days.items():
        if Day_OBJ["Accrued_Holiday"]:
            Days.append(Accrued_Holiday(Day_OBJ))
            continue

        if not Day_OBJ["IsValid"]:
            Days.append(Day_OBJ)
            continue

        # present on Holiday
        if Day_OBJ["Holiday"]:
            Total_Holiday += 1
            Day_OBJ["Off_Day"] = Day_OBJ["present_time"]

        # Not Present on working day
        elif not Day_OBJ["EnterExit"]:
            Day_OBJ["Undertime"] = EMP_Salary.Regular_hours_cap

        # Present on working day
        else:
            EnterExit = Day_OBJ["EnterExit"]
            WorkingHours, NonWorkingHours = [], []
            END = EMP_Salary.day_ending_time
            EnterExit.sort()

            for H in EnterExit:
                (WorkingHours if H <= END else NonWorkingHours).append(H)

            if len(WorkingHours) % 2:
                WorkingHours.append(END)
            if len(NonWorkingHours) % 2:
                NonWorkingHours.append(END)

            WorkingHours.sort()
            NonWorkingHours.sort()

            WorkingHours[0] = max(WorkingHours[0], EMP_Salary.day_starting_time)

            # UnderTime
            tmp_undertime = time_gap(EMP_Salary.day_starting_time, WorkingHours[0])
            Day_OBJ["delay"] = tmp_undertime
            if tmp_undertime > EMP_Salary.undertime_threshold:
                Day_OBJ["Undertime"] += tmp_undertime

            if WorkingHours[-1] < EMP_Salary.day_ending_time:
                tmp_undertime = time_gap(WorkingHours[-1], EMP_Salary.day_ending_time)
                Day_OBJ["haste"] = tmp_undertime
                if tmp_undertime > EMP_Salary.undertime_threshold:
                    Day_OBJ["Undertime"] += tmp_undertime

            # check if more than one Enter and Exit is in day
            if WorkingHours:
                for Enter, Exit in zip(WorkingHours[:-1:2], WorkingHours[1::2]):
                    Day_OBJ["Regular_hours"] += time_gap(Enter, Exit)

            Day_OBJ["Undertime"] = EMP_Salary.Regular_hours_cap - Day_OBJ["Regular_hours"]

            possible_overtime = 0
            if NonWorkingHours:
                for Enter, Exit in zip(NonWorkingHours[:-1:2], NonWorkingHours[1::2]):
                    possible_overtime += time_gap(Enter, Exit)

            if possible_overtime > EMP_Salary.overtime_threshold:
                Day_OBJ["Overtime"] = possible_overtime

        Days.append(finalize(Day_OBJ))
    return Days, Total_Holiday


def Split_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> Tuple[List[Dict], int]:
    Total_Holiday = 0
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
            Total_Holiday += 1
            Day_OBJ["Off_Day"] = Day_OBJ["present_time"]
        else:
            Regular_hours_cap = EMP_Salary.Regular_hours_cap
            if Day_OBJ["present_time"] >= Regular_hours_cap:
                possible_Overtime = Day_OBJ["present_time"] - Regular_hours_cap
                Day_OBJ["Overtime"] = possible_Overtime if possible_Overtime >= EMP_Salary.overtime_threshold else 0
            else:
                possible_undertime = Regular_hours_cap - Day_OBJ["present_time"]
                Day_OBJ["Undertime"] = possible_undertime if possible_undertime >= EMP_Salary.undertime_threshold else 0
            Day_OBJ["Regular_hours"] = min(Regular_hours_cap, Day_OBJ["present_time"])

        Days.append(finalize(Day_OBJ))
    return Days,Total_Holiday


@DEV_io()
def Hourly_schedule(EMP_Salary: dbm.Salary_Policy_form, preprocess_Days) -> Tuple[List[Dict], int]:
    Days = []
    for Date, Day_OBJ in preprocess_Days.items():
        if Day_OBJ["Accrued_Holiday"]:
            Days.append(Accrued_Holiday(Day_OBJ))
            continue

        if not Day_OBJ["IsValid"]:
            Days.append(Day_OBJ)
            continue

        if Day_OBJ["Holiday"]:
            Day_OBJ["Off_Day"] = Day_OBJ["present_time"]

        else:  # NC: 005
            if Day_OBJ["present_time"] >= EMP_Salary.Regular_hours_cap:
                possible_Overtime = Day_OBJ["present_time"] - EMP_Salary.Regular_hours_cap
                Day_OBJ["Overtime"] = possible_Overtime if possible_Overtime >= EMP_Salary.overtime_threshold else 0
            else:
                possible_undertime = EMP_Salary.Regular_hours_cap - Day_OBJ["present_time"]
                Day_OBJ["Undertime"] = possible_undertime if possible_undertime >= EMP_Salary.undertime_threshold else 0
                Day_OBJ["attendance_points"] -= 1

            Day_OBJ["Regular_hours"] = min(EMP_Salary.Regular_hours_cap, Day_OBJ["present_time"])
        Days.append(finalize(Day_OBJ))
    return Days, 0


@DEV_io()
def generate_daily_report(Salary_Policy: dbm.Salary_Policy_form, Fingerprint_scanner_report: List[dbm.Fingerprint_Scanner_form], Activities: Dict):
    """
    Generate the daily report Base on Employee fingerprint scanner report
    """
    try:
        report_dicts: Dict[str, Dict] = preprocess_report(Fingerprint_scanner_report, Activities)

        # Split schedule and Fix schedule
        if Salary_Policy.Salary_Type == "Fixed":
            Days, Total_Holiday = Fixed_schedule(Salary_Policy, report_dicts)
        elif Salary_Policy.Salary_Type == "Split":
            Days, Total_Holiday = Split_schedule(Salary_Policy, report_dicts)
        elif Salary_Policy.Salary_Type == "Hourly":
            Days, Total_Holiday = Hourly_schedule(Salary_Policy, report_dicts)
        else:
            return 400, "Invalid Salary Type"

        Total_Activity = Sum_of_Activity(Salary_Policy, Days)
        income = Calculate_income(Salary_Policy, Total_Activity, Total_Holiday)

        return 200, {"Days": Days, "Total_Holiday": Total_Holiday, **Total_Activity, **income}
    except Exception as e:
        return Return_Exception(Error=e)
