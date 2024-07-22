import re
from datetime import datetime, timedelta, time, date
from functools import wraps
from typing import List, Dict

DAYS_OF_WEEK = {
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    0: "Saturday",
    1: "Sunday",
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
    "1402-11-21",
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
    "2024-02-10",
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

datetime_pattern = re.compile(r'(\d{4})\D(\d{2})\D(\d{2})\D(\d{2}):(\d{2}):(\d{2})')
date_pattern = re.compile(r'(\d{4})\D(\d{2})\D(\d{2})')
time_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})')

__all__ = [
    "Fix_date",
    "Fix_time",
    "Fix_datetime",
    "Separate_days_by_DayCap",
    "Separate_days_by_Time",
    "Separate_days",
    "generate_month_interval",
    "generate_time_table",
    "same_month",
    "time_gap",
    "is_off_day",
    "to_persian",
    "to_international",
]


def Debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        return result

    return wrapper


def Fix_time(time_obj: str | datetime | time):
    if isinstance(time_obj, time):
        return time_obj.replace(second=0)
    if isinstance(time_obj, datetime):
        return time_obj.time().replace(second=0)
    time_obj = time_obj.replace("T", " ") if "T" in time_obj else time_obj
    if " " in time_obj:
        time_obj = time_pattern.match(time_obj)
    else:
        time_obj = time_pattern.match(time_obj)

    if not time_obj:
        raise ValueError(f"Incorrect data format, should be HH:MM:SS or HH:MM:SS.MMM, received: {time_obj}")
    time_obj = time_obj.groups()
    return time(hour=int(time_obj[-3]), minute=int(time_obj[-2]), second=int(time_obj[-1]))


def Fix_date(time_obj: str | datetime | date):
    if isinstance(time_obj, date):
        return time_obj
    if isinstance(time_obj, datetime):
        return time_obj.date()
    time_obj = time_obj.replace("T", " ") if "T" in time_obj else time_obj

    if " " in time_obj:
        time_obj = date_pattern.match(time_obj)
    else:
        time_obj = date_pattern.match(time_obj)

    if not time_obj:
        raise ValueError(f"Incorrect data format, should be YYYY:MM:DD, received: {time_obj}")
    time_obj = time_obj.groups()
    return date(year=int(time_obj[0]), month=int(time_obj[1]), day=int(time_obj[2]))


def Fix_datetime(time_obj: str | datetime):
    try:
        if isinstance(time_obj, datetime):
            return time_obj
        time_obj = time_obj.replace("T", " ") if "T" in time_obj else time_obj
        time_str = datetime_pattern.match(time_obj)
        if time_str is None:
            return

        time_str = time_str.groups()
        return datetime(year=int(time_str[0]), month=int(time_str[1]), day=int(time_str[2]), hour=int(time_str[3]), minute=int(time_str[4]), second=int(time_str[5]))
    except Exception as e:
        raise ValueError(f"Incorrect data format, should be YYYY-MM-DD HH:MM:SS or YYYY-MM-DD HH:MM:SS.MMM, received: {time_obj}\n{e}")


def is_off_day(day: date | datetime) -> bool:
    day = day if isinstance(day, date) else day.date()
    if day.weekday() == 4:
        return True
    if str(day) in holidays:
        return True
    return False


def time_gap(start: time | str, end: time | str) -> int:
    """
    return time gap in minutes
    """
    start, end = Fix_time(start), Fix_time(end)

    if end == time.max:
        return abs(1440 - start.hour * 60 + start.minute)
    return abs((end.hour * 60 + end.minute) - start.hour * 60 + start.minute)


def Separate_days_by_Time(start, end, day_starting_time: time, day_ending_time: time):
    start, end = Fix_datetime(start), Fix_datetime(end)
    daily = []

    while start.date() < end.date():
        daily.append({"Date": start.date(), "is_holiday": is_off_day(start.date()), "start": start.time(), "end": day_ending_time, "duration": time_gap(start.time(), day_ending_time)})
        start += timedelta(days=1)
        start = datetime.combine(start.date(), day_starting_time)

    daily.append({"Date": start.date(), "is_holiday": is_off_day(start.date()), "start": start.time(), "end": end.time(), "duration": time_gap(start.time(), min(end.time(), day_ending_time))})
    return daily


def Separate_days_by_DayCap(start, end, Working_cap: int) -> List[Dict]:
    start, end = Fix_datetime(start), Fix_datetime(end)
    daily = []

    while start.date() <= end.date():
        daily.append({"Date": start.replace(hour=0, minute=0, second=0, microsecond=0), "is_holiday": is_off_day(start.date()), "duration": Working_cap})
        start += timedelta(days=1)
    return daily


def Separate_days(start, end):
    def Day(D: date, S: time = time.min, E: time = time.max) -> Dict:
        return {"date": D, "start": S, "end": E.replace(second=0, microsecond=0), "duration": time_gap(S, E)}

    start, end = Fix_datetime(start), Fix_datetime(end)

    if start.date() == end.date():
        return [Day(start.date(), start.time(), end.time())]

    daily = [Day(D=start.date(), S=start.time())]
    daily.extend([Day(D=(start.date() + timedelta(days=i))) for i in range(1, (end.date() - start.date()).days)])
    daily.append(Day(D=start.date(), E=end.time()))

    return daily


def to_persian(year, month, day, return_obj=True) -> tuple | date:
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

    if return_obj:
        return date(jy, jm, jd)
    return jy, jm, jd


def to_international(year, month, day, return_obj=True) -> tuple | date:
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

    if return_obj:
        return date(year, month, day)
    return year, month, day


def generate_month_interval(year, month, include_nex_month_fist_day: bool = False) -> tuple[date, date]:
    """
    this function takes a year and month and returns two date object representing the start and end of the month
    """

    end_year = year + 1 if month == 12 else year
    end_month = 1 if month == 12 else month + 1

    start_date = to_international(year, month, 1)
    end_date = to_international(end_year, end_month, 1)
    if not include_nex_month_fist_day:
        end_date = end_date - timedelta(days=1)
    return start_date, end_date


def same_month(date_1: datetime, date_2: datetime):
    y1, m1, _ = to_persian(date_1.year, date_1.month, date_1.day, return_obj=False)
    y2, m2, _ = to_persian(date_2.year, date_2.month, date_2.day, return_obj=False)

    return y1 == y2 and m1 == m2


def generate_time_table(starting_date: date, ending_date: date, day_of_week=None) -> list:
    """
    Generate a time table between the starting_date and ending_date.

    Parameters:
        starting_date (date): The starting date of the time table.
        ending_date (date): The ending date of the time table.
        day_of_week (list, optional): A list of integers representing the days of the week. Defaults to None.

    Returns:
        list: A list of dictionaries containing the date and a boolean indicating if it's a holiday.
    """
    if day_of_week is None:
        day_of_week = [0, 1, 2, 3, 4, 5, 6]
    starting_date, ending_date = Fix_date(starting_date), Fix_date(ending_date)
    Days = []
    while starting_date <= ending_date:
        week_day = (starting_date.weekday() + 2) % 7
        if not is_off_day(starting_date) and week_day in day_of_week:
            Days.append((starting_date, week_day))
        starting_date += timedelta(days=1)
    return Days


if __name__ == '__main__':
    print(time.max)
    print(time_gap(time.min, time.max))
