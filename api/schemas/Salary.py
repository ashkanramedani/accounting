from typing import Dict

from pydantic import NonNegativeFloat, NonPositiveFloat

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
    Base_salary: NonNegativeFloat
    Regular_hours_factor: NonNegativeFloat
    Fix_pay: NonNegativeFloat

    overtime_permission: bool
    overtime_factor: NonNegativeFloat
    overtime_cap: NonNegativeFloat
    overtime_threshold: int

    undertime_factor: NonNegativeFloat
    undertime_threshold: int

    # off_Day
    off_day_permission: bool
    off_day_factor: NonNegativeFloat
    off_day_cap: NonNegativeFloat

    # Remote
    remote_permission: bool
    remote_factor: NonNegativeFloat
    remote_cap: NonNegativeFloat

    # Leave_form
    medical_leave_factor: NonNegativeFloat
    medical_leave_cap: NonNegativeFloat

    vacation_leave_factor: NonNegativeFloat
    vacation_leave_cap: NonNegativeFloat

    # business_Trip
    business_trip_permission: bool
    business_trip_factor: NonNegativeFloat
    business_trip_cap: NonNegativeFloat


class post_SalaryPolicy_schema(SalaryPolicy):
    pass


class update_SalaryPolicy_schema(SalaryPolicy):
    salary_policy_pk_id: UUID


class SalaryPolicy_response(Base_response, update_SalaryPolicy_schema):
    employee: export_employee

    class Config:
        extra = 'ignore'
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


class employee_salary_Response(Base_response):
    employee_salary_pk_id: UUID
    employee: Employee_salary
    fingerprint_scanner_user_id: int

    present_time: int
    Regular_hours: int
    Overtime: int
    Undertime: int
    Off_Day: int

    delay: int
    haste: int
    attendance_points: int

    rewards_earning: NonNegativeFloat
    Fix_pay: NonNegativeFloat
    punishment_deductions: NonNegativeFloat

    Regular_earning: NonNegativeFloat
    Overtime_earning: NonNegativeFloat
    Off_Day_earning: NonNegativeFloat

    Undertime_deductions: NonNegativeFloat
    insurance_deductions: NonNegativeFloat
    tax_deductions: NonNegativeFloat

    remote: int
    vacation_leave: int
    medical_leave: int
    business_trip: int

    remote_earning: NonNegativeFloat
    vacation_leave_earning: int
    medical_leave_earning: int
    business_trip_earning: NonNegativeFloat

    total_earning: NonNegativeFloat
    total_deduction: NonNegativeFloat
    total_income: NonNegativeFloat

    card: Optional[export_payment]
    payment_date: Optional[date]

    class Config:
        extra = 'ignore'
        orm_mode = True

class teacher_salary_report(BaseModel):
    course_id: UUID
    Cancellation_factor: NonNegativeFloat
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
    Does_Have_Salary_Policy: bool
    role: Optional[Any] = None

    class Config:
        extra = 'ignore'
        orm_mode = True


class permission_response(BaseModel):
    remote_permission: bool
    business_trip_permission: bool
    salary_Policy: bool

    class Config:
        extra = 'ignore'
        orm_mode = True


#  Teacher
class Teacher_course_report(Base_response):
    course_pk_id: UUID
    course_name: str
    course_image: str
    starting_date: date
    ending_date: date
    course_capacity: NonNegativeInt
    course_level: str
    course_code: int

    language: export_language
    type: export_course_type


class Teacher_subcourse_report(Base_response):
    sub_course_pk_id: UUID
    sub_course_name: str
    create_date: datetime

    sub_course_starting_date: date
    sub_course_ending_date: date
    note: Dict

    sub_teachers: List[export_employee]
    teacher: export_employee
    course: export_course


###

class update_employee_salary(BaseModel):
    rewards_earning: NonNegativeFloat = 0
    punishment_deductions: NonNegativeFloat = 0
    loan_installment: NonNegativeFloat = 0
    payment: UUID
    payment_date: date | str

    class Config:
        extra = 'ignore'
