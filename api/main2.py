from db import models
from db.models import SessionLocal
from lib import *

db = SessionLocal()
# Ensure you import the necessary modules

# Proper query to avoid Cartesian product
Start, End = Fix_datetime("2024-06-13T14:20:56.666871"), Fix_datetime("2024-06-14T14:20:56.666880")

if End < Start:
    print(400, "Bad Request: End Date must be greater than Start Date")

if not same_month(Start, End):
    print(400, f"Bad Request: End Date must be in the same month as Start Date: {Start}, {End}")

# this part check if leave request is daily or hourly
if End.date() == Start.date():
    if not is_off_day(Start):
        OBJ = dbm.Leave_Request_form(start_date=Start.time(), end_date=End.time(), duration=(End - Start).total_seconds() // 60, date=Start.replace(hour=0, minute=0, second=0, microsecond=0), **data)  # type: ignore[call-arg]
        db.add(OBJ)
else:
    OBJ = []
    Salary_Obj = db.query(models.Salary_Policy_form).filter_by(user_fk_id="308e2744-833c-4b94-8e27-44833c2b940f", deleted=False).first()
    if not Salary_Obj:
        print(400, "Bad Request: Employee Does Not Have Employee_Salary_form Record")
    for day in Separate_days_by_DayCap(Start, End, Salary_Obj.Regular_hours_cap):
        if not day["is_holiday"]:
            OBJ.append(dbm.Leave_Request_form(start_date=time(0, 0, 0), end_date=time(23, 59, 59), date=day["Date"], duration=day["duration"], **data))  # type: ignore[call-arg]
#
#     db.add_all(OBJ)
# db.commit()

#
# Unique_EnNo = [5, 4, 16, 15, 6, 12, 3, 17, 11, 10, 13, 9, 7]
# User_name = ['E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R']
# salaries = [(UUID('b23ff8ea-7aa5-4b9a-b7f2-94c066f47e4c'),), (UUID('faf9d261-54b3-4602-aac6-f7d3c935a716'),)]
# Salary_Result = ['b23ff8ea-7aa5-4b9a-b7f2-94c066f47e4c', 'faf9d261-54b3-4602-aac6-f7d3c935a716']
# Result = {'E': False, 'F': False, 'G': False, 'H': False, 'J': False, 'K': False, 'L': False, 'M': False, 'N': False, 'P': False, 'Q': False, 'R': False}