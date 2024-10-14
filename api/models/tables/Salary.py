from sqlalchemy import TIME, Float, Date
from sqlalchemy.orm import relationship

from .Base_form import *


class Salary_Policy_form(Base, Base_form):
    __tablename__ = "salary_policy"
    salary_policy_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")
    user_fk_id = create_foreignKey("User_form")

    Base_salary = Column(Float, nullable=False)
    Fix_pay = Column(Float, nullable=False, default=0)
    Salary_Type = Column(String, nullable=False, default="Fixed")  # Fixed, Hourly, Split

    day_starting_time = Column(TIME, nullable=True, default=None)
    day_ending_time = Column(TIME, nullable=True, default=None)

    # finger_print
    Regular_hours_factor = Column(Float, nullable=False)
    Regular_hours_cap = Column(Integer, nullable=False)

    overtime_permission = Column(Boolean, nullable=False)
    overtime_factor = Column(Float, nullable=False)
    overtime_cap = Column(Integer, nullable=False)
    overtime_threshold = Column(Integer, nullable=False)

    undertime_factor = Column(Float, nullable=False)
    undertime_threshold = Column(Integer, nullable=False)

    # off day work
    off_day_permission = Column(Boolean, nullable=False)
    off_day_factor = Column(Float, nullable=False)
    off_day_cap = Column(Integer, nullable=False)

    # Remote
    remote_permission = Column(Boolean, nullable=False)
    remote_factor = Column(Float, nullable=False)
    remote_cap = Column(Integer, nullable=False)

    # Leave_form
    medical_leave_factor = Column(Float, nullable=False)
    medical_leave_cap = Column(Integer, nullable=False)

    vacation_leave_factor = Column(Float, nullable=False)
    vacation_leave_cap = Column(Integer, nullable=False)

    # business_Trip
    business_trip_permission = Column(Boolean, nullable=False)
    business_trip_factor = Column(Float, nullable=False)
    business_trip_cap = Column(Integer, nullable=False)

    employee = relationship("User_form", foreign_keys=[user_fk_id])
    created = relationship("User_form", foreign_keys=[created_fk_by])

    def summery(self) -> dict:
        def Validate(key: str):
            for invalid_key in ["_fk_", "_pk_", "_sa_instance_"]:
                if invalid_key in key:
                    return False
            return True

        return {k: str(v) for k, v in self.__dict__.items() if Validate(k)}

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teachers_Report_form(Base, Base_form):
    __tablename__ = "teachers_report"
    # __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    teachers_report_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    teacher_fk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    score = Column(Float)
    number_of_student = Column(Integer)
    canceled_course = Column(Integer, default=0)
    replaced_course = Column(Integer, default=0)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)

    # ++++++++++++++++++++++++++ Survey +++++++++++++++++++++++++++

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Employee_Salary_form(Base, Base_form):
    __tablename__ = "employee_salary"
    __table_args__ = (UniqueConstraint('user_fk_id', 'year', 'month'),)

    employee_salary_pk_id = create_Unique_ID()
    fingerprint_scanner_user_id = Column(Integer, nullable=True)

    user_fk_id = create_foreignKey("User_form")

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    payment = create_foreignKey("Payment_Method_form", nullable=True)
    payment_date = Column(Date, nullable=True)
    rewards_earning = Column(Float, nullable=False, default=0)
    punishment_deductions = Column(Float, nullable=False, default=0)
    loan_installment = Column(Float, nullable=False, default=0)

    present_time = Column(Integer, nullable=False)
    Regular_hours = Column(Integer, nullable=False)
    Overtime = Column(Integer, nullable=False)
    Undertime = Column(Integer, nullable=False)
    Off_Day = Column(Integer, nullable=False)

    delay = Column(Integer, nullable=False)
    haste = Column(Integer, nullable=False)

    attendance_points = Column(Integer, nullable=False, default=0)
    Fix_pay = Column(Float, nullable=False, default=0)

    Regular_earning = Column(Float, nullable=False)
    Overtime_earning = Column(Float, nullable=False)
    Off_Day_earning = Column(Float, nullable=False)

    Undertime_deductions = Column(Float, nullable=False)
    insurance_deductions = Column(Float, nullable=False)
    tax_deductions = Column(Float, nullable=False)

    remote = Column(Integer, nullable=False)
    vacation_leave = Column(Integer, nullable=False)
    medical_leave = Column(Integer, nullable=False)
    business_trip = Column(Integer, nullable=False)

    remote_earning = Column(Float, nullable=False)
    vacation_leave_earning = Column(Integer, nullable=False)
    medical_leave_earning = Column(Float, nullable=False)
    business_trip_earning = Column(Float, nullable=False)

    total_earning = Column(Float, nullable=False)
    total_deduction = Column(Float, nullable=False)
    total_income = Column(Float, nullable=False)

    Salary_Policy = Column(JSON, nullable=False)
    Days = Column(JSON, nullable=False)

    employee = relationship("User_form", foreign_keys=[user_fk_id])
    card = relationship("Payment_Method_form", foreign_keys=[payment])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teacher_salary_form(Base, Base_form):
    __tablename__ = "teacher_salary"
    # __table_args__ = (UniqueConstraint('user_fk_id', 'subcourse_fk_id'),)
    teacher_salary_pk_id = create_Unique_ID()

    user_fk_id = create_foreignKey("User_form")
    subcourse_fk_id = create_foreignKey("Sub_Course_form")

    course_data = Column(JSON, nullable=False)
    total_sessions = Column(Integer, nullable=False)

    payment = create_foreignKey("Payment_Method_form", nullable=True)
    payment_date = Column(Date, nullable=True)
    rewards_earning = Column(Float, nullable=False, default=0)
    punishment_deductions = Column(Float, nullable=False, default=0)
    loan_installment = Column(Float, nullable=False, default=0)

    roles_score = Column(Float, nullable=False)
    survey_score = Column(Float, nullable=False)
    course_level_score = Column(Float, nullable=False)
    tardy_score = Column(Float, nullable=False)
    content_creation = Column(Float, nullable=False)
    event_participate = Column(Float, nullable=False)
    CPD = Column(Float, nullable=False)
    Odd_hours = Column(Float, nullable=False)
    report_to_student = Column(Float, nullable=False)
    LP_submission = Column(Float, nullable=False)
    student_assign_feedback = Column(Float, nullable=False)
    result_submission_to_FD = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    SUB = Column(Boolean, nullable=False)
    sub_point = Column(Float, nullable=False)
    ID_Experience = Column(Integer, nullable=False)
    experience_gain = Column(Integer, nullable=False)
    attended_session = Column(Integer, nullable=False)
    roles = Column(JSON, nullable=False)
    score = Column(Float, nullable=False)
    earning = Column(Float, nullable=False)

    BaseSalary = Column(Float, nullable=False)
    session_cancellation_deduction = Column(Float, nullable=False)

    card = relationship("Payment_Method_form", foreign_keys=[payment])
    teacher = relationship("User_form", foreign_keys=[user_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[subcourse_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)
