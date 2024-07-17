from datetime import datetime

from pydantic import PositiveInt

from .Base import *


class salary_type(Enum):
    Fixed = "Fixed"
    Split = "Split"
    Hourly = "Hourly"


# ---------------------- Employee_Salary_form ----------------------
class SalaryPolicy(Base_form):
    user_fk_id: UUID

    day_starting_time: Optional[time | str | None] = None
    day_ending_time: Optional[time | str | None] = None
    Regular_hours_cap: Optional[int | None] = None
    Salary_Type: str

    # finger_print
    Base_salary: float
    Regular_hours_factor: float

    overtime_permission: bool
    overtime_factor: float
    overtime_cap: float
    overtime_threshold: int

    undertime_factor: float
    undertime_threshold: int

    # off_Day
    off_day_permission: bool
    off_day_factor: float
    off_day_cap: float

    # Remote
    remote_permission: bool
    remote_factor: float
    remote_cap: float

    # Leave_form
    medical_leave_factor: float
    medical_leave_cap: float

    vacation_leave_factor: float
    vacation_leave_cap: float

    # business_Trip
    business_trip_permission: bool
    business_trip_factor: float
    business_trip_cap: float


class post_SalaryPolicy_schema(SalaryPolicy):
    pass


class update_SalaryPolicy_schema(SalaryPolicy):
    salary_policy_pk_id: UUID


class SalaryPolicy_response(Base_response, update_SalaryPolicy_schema):
    employee: export_employee

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ Employee_Salary_form +++++++++++++++++++++++++++
class salary_report(BaseModel):
    user_fk_id: UUID
    year: PositiveInt
    month: PositiveInt


class teacher_report(BaseModel):
    teacher_fk_id: UUID
    start_date: Any
    end_date: Any


class employee_report(BaseModel):
    user_fk_id: UUID
    start_date: datetime | str
    end_date: datetime | str


class teacher_salary_report(BaseModel):
    course_id: UUID
    Cancellation_factor: float
    StudentAssignFeedback: str
    LP_submission: str
    result_submission_to_FD: str
    ReportToStudent: str


# ---------------------- course cancellation ---------------------
class Input(BaseModel):
    year: PositiveInt
    month: PositiveInt


class Return_Salary(export_employee):
    Does_Have_Salary_Record: bool
    role: Optional[Any] = None

    class Config:
        orm_mode = True


class permission_response(BaseModel):
    remote_permission: Optional[bool] = False
    business_trip_permission: Optional[bool] = False

    class Config:
        orm_mode = True
