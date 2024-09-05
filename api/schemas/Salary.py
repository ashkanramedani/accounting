from .Base import *


# ---------------------- Salary_form ----------------------
class SalaryPolicy(BaseModel):
    created_fk_by: UUID
    user_fk_id: UUID

    day_starting_time: time | None | str = None
    day_ending_time: time | None | str = None

    # finger_print
    Base_salary: float
    Regular_hours_factor: float
    Regular_hours_cap: Optional[int] = None

    overtime_permission: bool
    overtime_factor: float
    overtime_cap: int
    overtime_threshold: int

    undertime_factor: float
    undertime_threshold: int

    # off_Day
    off_day_permission: bool
    off_day_factor: float
    off_day_cap: int

    # Remote
    remote_permission: bool
    remote_factor: float
    remote_cap: int

    # Leave_form
    medical_leave_factor: float
    medical_leave_cap: int

    vacation_leave_factor: float
    vacation_leave_cap: int

    # business_Trip
    business_trip_permission: bool
    business_trip_factor: float
    business_trip_cap: int


class post_SalaryPolicy_schema(SalaryPolicy):
    pass


class update_SalaryPolicy_schema(SalaryPolicy):
    salary_policy_pk_id: UUID


class SalaryPolicy_response(Base_response, update_SalaryPolicy_schema):
    employee: export_employee

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ Salary_form +++++++++++++++++++++++++++
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
    Base_salary: int | float
    teacher_level: int | float
    course_cap: int | float
    StudentAssignFeedback: int | float
    course_level: int | float
    course_type: int | float
    survey_score: int | float
    LP_submission: int | float
    result_submission_to_FD: int | float
    course_cancellation: int | float
    ReportToStudent: int | float
    time_management: int | float
