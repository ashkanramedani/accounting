from typing import Literal

from pydantic import NonNegativeFloat, root_validator

from .Base import *


class salary_type(Enum):
    Fixed = "Fixed"
    Split = "Split"
    Hourly = "Hourly"


# ---------------------- Employee_Salary_form ----------------------
class SalaryPolicy(Base_form):
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
    user_fk_id: UUID
    day_starting_time: Optional[time | str | None] = None
    day_ending_time: Optional[time | str | None] = None
    Regular_hours_cap: Optional[int | None] = None
    Salary_Type: Literal["Fixed", "Split", "Hourly"]


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
    #
    remote_earning: NonNegativeFloat
    vacation_leave_earning: int
    medical_leave_earning: int
    business_trip_earning: NonNegativeFloat
    #
    total_earning: float
    total_deduction: float
    total_income: float
    #
    card: Optional[export_payment | None] = None
    payment_date: date | None = None
    #
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
    course_code: str

    language: export_language
    type: export_course_type


class Teacher_subcourse_report(BaseModel):
    sub_course_pk_id: UUID
    sub_course_name: str
    create_date: datetime

    sub_course_starting_date: date
    sub_course_ending_date: date

    Does_Have_Salary_Record: bool = False

    sub_teachers: List[export_employee]
    teacher: export_employee
    course: export_course


###

class update_salary_report(BaseModel):
    rewards_earning: NonNegativeFloat = 0
    punishment_deductions: NonNegativeFloat = 0
    loan_installment: NonNegativeFloat = 0
    payment: UUID
    payment_date: date | str

    class Config:
        extra = 'ignore'


class four_Option(Enum):
    weak = "weak"
    average = "average"
    good = "good"
    excellent = "excellent"


class three_Option(Enum):
    weak = "weak"
    average = "average"
    good = "good"


class teacher_salary_DropDowns(BaseModel):
    CPD: float = 0.0
    Odd_hours: float = 0.0
    rewards_earning: float = 0.0
    content_creation: float = 0.0
    event_participate: float = 0.0

    survey_score: four_Option = "average"
    LP_submission: four_Option = "average"
    report_to_student: four_Option = "average"
    student_assign_feedback: four_Option = "average"
    result_submission_to_FD: three_Option = "average"

    @root_validator(pre=True)
    def check_values(cls, values):
        for field, value in values.items():
            if field in ["CPD", "Odd_hours", "content_creation", "event_participate"]:
                if 0 > value or value > 100:
                    raise ValueError(f'{field} must be between 0 and 100')
            if field in ["cancellation_factor"]:
                if 0 > value or value > 10:
                    raise ValueError(f'{field} must be between 0 and 10')
        return values

    class Config:
        orm_mode = True


class Report(BaseModel):  # course_data_for_report):
    name: str
    SUB: bool
    sub_point: int = 0
    ID_Experience: int
    experience_gain: int = 0
    attended_session: int = 0
    total_sessions: int = 0
    roles_score: float = 0
    roles: Optional[Dict] = {}

    @root_validator(pre=True)
    def flatten_type(cls, values):
        # Unpack Teacher data
        values["name"] = f'{values["name"]} {values["last_name"]}'
        if values["roles"]:
            values["roles_score"] = sum(i.value for i in values["roles"])
            values["roles"] = {f'{i.cluster}_{i.name}': i.value for i in values["roles"]}

        return values

    class Config:
        orm_mode = True
        extra = 'ignore'


class EMP(BaseModel):
    user_pk_id: UUID
    name: str
    last_name: str


class Teacher_report_response(BaseModel):
    teacher_salary_pk_id: UUID

    user_fk_id: UUID
    subcourse_fk_id: UUID

    # name: str
    # SUB: bool
    # ID_Experience: int
    # experience_gain: int
    # attended_session: int
    #
    # payment: Optional[UUID]
    # payment_date: Optional[date]
    # rewards_earning: float = 0
    # loan_installment: float = 0
    # punishment_deductions: float = 0
    #
    # tardy: int
    # tardy_score: float
    #
    # sub_point: float
    # cancelled_session: int
    #
    # roles: Dict
    # roles_score: float
    #
    # BaseSalary: float
    #
    # # from user
    # CPD: float
    # Odd_hours: float
    # survey_score: float
    # LP_submission: float
    # content_creation: float
    # report_to_student: float
    # event_participate: float
    # course_level_score: float
    # cancellation_factor: float
    # result_submission_to_FD: float
    # student_assign_feedback: float

    score: float
    earning: float
    #
    # card: export_payment
    teacher: export_employee

    # sub_course: export_sub_course

    class Config:
        extra = 'ignore'
        orm_mode = True
