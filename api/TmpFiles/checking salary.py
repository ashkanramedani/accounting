from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NegativeFloat, NonPositiveFloat

class employee_salary(BaseModel):
    a: NonPositiveFloat = 0
    b: Optional[NonPositiveFloat]


for i in range(-2, 2):
    try:
        print(employee_salary())
    except Exception as e:
        print(i, e.__repr__())


class employee_salary_form(BaseModel):
    employee_salary_pk_id: UUID
    create_date: datetime  # <-----
    employee: str = "Employee"

    total_income: float
    total_earning: float
    total_deductions: float

    Off_Day_earning: float
    remote_earning: float
    Regular_earning: float
    Overtime_earning: float
    business_trip_earning: float
    medical_leave_earning: float
    vacation_leave_earning: float

    Undertime_earning: NonPositiveFloat
    insurance: Optional[NonPositiveFloat] = 0  # <----- Should be added
    tax: Optional[NonPositiveFloat] = 0  # <----- Should be added

    regular_work_time: 2940
    present_time: 3360
    business_trip: 1
    overtime: 0
    remote: 1
    undertime: 0
    off_Day_work_time: 1
    vacation_leave: -959
    medical_leave: -959
