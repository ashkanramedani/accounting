import json
from functools import wraps

from faker import Faker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date
from typing import List, Dict
from uuid import UUID
from random import choice as r_ch
import schemas as sch
import db.models as dbm
from lib import logger


Tables = {
    "survey": dbm.Survey_form,
    "Post": dbm.Posts,
    "role": dbm.Roles_form,
    "Remote Request": dbm.Remote_Request_form,
    "question": dbm.Questions_form,
    "response": dbm.Response_form,
    "Business Trip": dbm.Business_Trip_form,
    "Class Cancellation": dbm.Class_Cancellation_form,
    "Employee": dbm.Employees_form,
    "Tardy Request": dbm.Teacher_tardy_reports_form,
    "Student": dbm.Student_form,
    "Teacher Replacement": dbm.Teacher_Replacement_form,
    "class": dbm.Class_form,
    "fingerprint_scanner": dbm.Fingerprint_scanner_form,
    "payment_method": dbm.Payment_method_form,
    "Leave Forms": dbm.Leave_request_form
}

holidays = [
        "1402-01-01",
        "1402-01-02",
        "1402-01-03",
        "1402-01-04",
        "1402-01-12",
        "1402-01-13",
        "1402-01-23",
        "1402-02-02",
        "1402-02-03",
        "1402-02-26",
        "1402-03-14",
        "1402-03-15",
        "1402-04-08",
        "1402-04-16",
        "1402-05-05",
        "1402-05-06",
        "1402-06-15",
        "1402-06-23",
        "1402-06-25",
        "1402-07-02",
        "1402-07-11",
        "1402-08-26",
        "1402-11-05",
        "1402-11-19",
        "1402-11-22",
        "1402-12-06",
        "1402-12-29",
        "2023-03-21",
        "2023-03-22",
        "2023-03-23",
        "2023-03-24",
        "2023-04-01",
        "2023-04-02",
        "2023-04-12",
        "2023-04-22",
        "2023-04-23",
        "2023-05-16",
        "2023-06-04",
        "2023-06-05",
        "2023-06-29",
        "2023-07-07",
        "2023-07-27",
        "2023-07-28",
        "2023-09-06",
        "2023-09-14",
        "2023-09-16",
        "2023-09-24",
        "2023-10-03",
        "2023-11-17",
        "2024-01-25",
        "2024-02-08",
        "2024-02-11",
        "2024-02-25",
        "2024-03-19",
        "1403-01-01",
        "2024-03-20",
        "1403-01-02",
        "2024-03-21",
        "1403-01-03",
        "2024-03-22",
        "1403-01-04",
        "2024-03-23",
        "1403-01-12",
        "2024-03-31",
        "1403-01-13",
        "2024-04-01",
        "1403-01-22",
        "2024-04-10",
        "1403-01-23",
        "2024-04-11",
        "1403-02-15",
        "2024-05-04",
        "1403-03-14",
        "2024-06-03",
        "1403-03-15",
        "2024-06-04",
        "1403-03-28",
        "2024-06-17",
        "1403-04-05",
        "2024-06-25",
        "1403-04-25",
        "2024-07-15",
        "1403-04-26",
        "2024-07-16",
        "1403-05-04",
        "2024-07-25",
        "1403-06-12",
        "2024-09-02",
        "1403-06-14",
        "2024-09-04",
        "1403-06-22",
        "2024-09-12",
        "1403-07-31",
        "2024-10-22",
        "1403-09-15",
        "2024-12-05",
        "1403-10-25",
        "2025-01-14",
        "1403-11-09",
        "2025-01-28",
        "1403-11-22",
        "2025-02-10",
        "1403-11-26",
        "2025-02-14",
        "1403-12-29",
        "2025-03-19",
        "1403-12-30",
        "2025-03-20"
    ]

__all__ = [
    "to_persian",
    "to_international",
    "employee_exist",
    "class_exist",
    'record_order_by',
    'Fix_time',
    'count',
    'Fix_datetime',
    'Fix_date',
    'Separate_days_by_Time',
    'Separate_days_by_DayCap',
    'generate_month_interval',
    'same_month',
    "_sub",
    "is_off_day",
    'Person',
    'JSONEncoder',
    'safe_run']

class Person:
    def __init__(self):
        self.unique_names = []
        self.fake = Faker()

    def iterate(self):
        return f'{self.fake.first_name()}-{self.fake.last_name()}'

    def generate_name(self, unique: bool = True):
        if not unique and self.unique_names:
            return r_ch(self.unique_names).split('-')
        tmp = self.iterate()
        while tmp in self.unique_names:
            tmp = self.iterate()
        self.unique_names.append(tmp)
        return tmp.split('-')

class JSONEncoder(json.JSONEncoder):
    """
    Handles Not Json compatible types by attempting to create string version
    """
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        return func(*args, **kwargs)

    return wrapper

def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True


def class_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.Class_form).filter_by(class_pk_id=FK_field, deleted=False).first():
        return False
    return True


def record_order_by(db: Session, table, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    if order == "desc":
        return db.query(table).filter_by(deleted=False).order_by(table.create_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return db.query(table).filter_by(deleted=False).order_by(table.create_date.asc()).offset((page - 1) * limit).limit(limit).all()


def Fix_time(time_obj: str | datetime | time):
    if isinstance(time_obj, time):
        return time_obj
    if isinstance(time_obj, datetime):
        return time_obj.time()
    time_obj = time_obj.replace("T", " ") if "T" in time_obj else time_obj
    try:
        if "." in time_obj:
            return datetime.strptime(time_obj, "%H:%M:%S.%f").replace(microsecond=0)
        return datetime.strptime(time_obj, "%H:%M:%S")
    except ValueError:
        raise ValueError(f"Incorrect data format, should be HH:MM:SS or HH:MM:SS.MMM, received: {time_obj}")


def Fix_date(time_obj: str | datetime | date):
    if isinstance(time_obj, date):
        return time_obj
    if isinstance(time_obj, datetime):
        return time_obj.date()
    time_obj = time_obj.replace("T", " ") if "T" in time_obj else time_obj
    try:
        if " " in time_obj:
            if "." in time_obj:
                return datetime.strptime(time_obj, "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0).date()
            return datetime.strptime(time_obj, "%Y-%m-%d %H:%M:%S").date()
        return datetime.strptime(time_obj, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Incorrect data format, should be HH:MM:SS or HH:MM:SS.MMM, received: {time_obj}")

def Fix_datetime(time: str | datetime):
    if isinstance(time, datetime):
        return time
    time = time.replace("T", " ") if "T" in time else time
    try:
        if "." in time:
            return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)
        return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"Incorrect data format, should be YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SS.MMM, received: {time}")


def is_off_day(day: date | datetime) -> bool:
    day = day if isinstance(day, date) else day.date()
    if day.weekday() == 4:
        return True
    if str(day) in holidays:
        return True
    return False

def count(db, field: str):
    if field not in Tables:
        return 404, "field Not Found"

    return 200, len(db.query(Tables[field]).filter_by(deleted=False).all())


def _sub(start: time, end: time):
    start = datetime.combine(datetime.today(), start)
    end = datetime.combine(datetime.today(), end)
    return (end - start).total_seconds() // 60


def Separate_days_by_Time(start, end, day_starting_time: time, day_ending_time: time):
    start, end = Fix_datetime(start), Fix_datetime(end)
    daily = []

    while start.date() < end.date():
        daily.append({"Date": start.date(), "is_holiday": is_off_day(start.date()), "start": start.time(), "end": day_ending_time, "duration": _sub(start.time(), day_ending_time)})
        start += timedelta(days=1)
        start = datetime.combine(start.date(), day_starting_time)

    daily.append({"Date": start.date(), "is_holiday": is_off_day(start.date()), "start": start.time(), "end": end.time(), "duration": _sub(start.time(), min(end.time(), day_ending_time))})
    return daily



def Separate_days_by_DayCap(start, end, Working_cap: int) -> List[Dict]:
    start, end = Fix_datetime(start), Fix_datetime(end)
    daily = []

    while start.date() <= end.date():
        daily.append({"Date": start.replace(hour=0, minute=0, second=0, microsecond=0), "is_holiday": is_off_day(start.date()), "duration": Working_cap})
        start += timedelta(days=1)
    return daily


def to_persian(year, month, day):
    d_4 = year % 4
    g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    doy_g = g_a[month] + day
    if d_4 == 0 and month > 2:
        doy_g += 1
    d_33 = int(((year - 16) % 132) * .0305)
    a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
    if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
        b = 78
    else:
        b = 80 if (d_33 == 3 and d_4 == 0) else 79
    if int((year - 10) / 63) == 30:
        a -= 1
        b += 1
    if doy_g > b:
        jy = year - 621
        doy_j = doy_g - b
    else:
        jy = year - 622
        doy_j = doy_g + a
    if doy_j < 187:
        jm = int((doy_j - 1) / 31)
        jd = doy_j - (31 * jm)
        jm += 1
    else:
        jm = int((doy_j - 187) / 30)
        jd = doy_j - 186 - (jm * 30)
        jm += 7

    return date(jy, jm, jd)


def to_international(year, month, day):
    d_4 = (year + 1) % 4
    doy_j = ((month - 1) * 31 + day) if month < 7 else ((month - 7) * 30 + day + 186)
    d_33 = int(((year - 55) % 132) * .0305)
    a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
    b = 78 if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1) else (80 if (d_33 == 3 and d_4 == 0) else 79)
    a -= 1 if int((year - 19) / 63) == 20 else 0
    b += 1 if int((year - 19) / 63) == 20 else 0
    year, day = (year + 621, doy_j + b) if doy_j <= a else (year + 622, doy_j - a)

    for month, v in enumerate([0, 31, 29 if (year % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
        if day <= v:
            break
        day -= v

    return date(year, month, day)


def generate_month_interval(year, month, include_nex_month_fist_day: bool = False) -> tuple[date, date]:
    end_year = year + 1 if month == 12 else year
    end_month = 1 if month == 12 else month + 1

    start_date = to_international(year, month, 1)
    end_date = to_international(end_year, end_month, 1)
    if not include_nex_month_fist_day:
        end_date = end_date - timedelta(days=1)
    return start_date, end_date


def same_month(date_1: datetime, date_2: datetime):
    date_1 = to_persian(date_1.year, date_1.month, date_1.day)
    date_2 = to_persian(date_2.year, date_2.month, date_2.day)
    return date_1.year == date_2.year and date_1.month == date_2.month

if __name__ == '__main__':
    for i in range(1, 13):
        a = generate_month_interval(1402, i)
        print(1402, i, a)
