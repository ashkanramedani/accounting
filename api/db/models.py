from enum import Enum as PythonEnum

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Enum, Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Time, MetaData, Float, Interval
from sqlalchemy.sql import expression, func

from .database import Base

metadata_obj = MetaData()

__all__ = [
    "BaseTable",
    "Leave_request_form",
    "Student_form",
    "Class_form",
    "Employees_form",
    "Remote_Request_form",
    "Teacher_tardy_reports_form",
    "Class_Cancellation_form",
    "Teacher_Replacement_form",
    "WeekdayEnum",
    "Day_form",
    "Employee_Timesheet_form",
    "Business_Trip_form",
    "Teachers_Report_form",
    "survey_form",
    "Questions_form",
    "survey_questions_form",
    "response_form"
]

IDs = {
    "employees": "employees.employees_pk_id",
    "classes": "classes.class_pk_id",
    "days": "days.day_pk_id",
    "employee_timesheet": "employee_timesheet.employee_timesheet_pk_id",
    "forms": "forms.form_pk_id",
    "question": "question.question_pk_id",
    "student": "student.student_pk_id"
}


def create_Unique_ID():
    return Column(GUID,
                  server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
                  primary_key=True,
                  nullable=False,
                  unique=True,
                  index=True)


def create_forenKey(table: str):
    return Column(GUID, ForeignKey(IDs[table], ondelete='SET NULL'), nullable=False)


class BaseTable:
    # __tablename__ = "BASE"
    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expire_date = Column(DateTime(timezone=True), default=None)
    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    # user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)
    # user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)


class Leave_request_form(Base, BaseTable):
    __tablename__ = "leave_request"
    leave_request_pk_id = create_Unique_ID()
    created_by_fk_id = create_forenKey("employees")
    created_for_fk_id = create_forenKey("employees")
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    Description = Column(String)


class Student_form(Base, BaseTable):
    __tablename__ = "student"
    student_pk_id = create_Unique_ID()
    student_name = Column(String, nullable=False)
    student_last_name = Column(String, index=True)
    student_level = Column(String, index=True)
    student_age = Column(Integer)


class Class_form(Base, BaseTable):
    __tablename__ = "classes"
    class_pk_id = create_Unique_ID()
    starting_time = Column(Time, nullable=False)
    duration = Column(Interval)
    class_date = Column(DateTime, nullable=True)


class Employees_form(Base, BaseTable):
    __tablename__ = "employees"
    employees_pk_id = create_Unique_ID()
    name = Column(String, nullable=False)
    last_name = Column(String, index=True)
    job_title = Column(String, index=True)


class Remote_Request_form(Base, BaseTable):
    __tablename__ = "remote_requests"
    remote_request_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    create_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    working_location = Column(String)
    description = Column(String)


class Teacher_tardy_reports_form(Base, BaseTable):
    __tablename__ = "teacher_tardy_reports"
    teacher_tardy_reports_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    delay = Column(Interval)


class Class_Cancellation_form(Base, BaseTable):
    __tablename__ = "class_cancellation"
    class_cancellation_pk_id = create_Unique_ID()
    created_date = Column(Date)
    created_fk_by = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    teacher_fk_id = create_forenKey("employees")
    replacement = Column(Date)
    class_duration = Column(Interval)
    class_location = Column(String)
    description = Column(String)


class Teacher_Replacement_form(Base, BaseTable):
    __tablename__ = "teacher_replacement"
    teacher_replacement_pk_id = create_Unique_ID()
    created_by_fk_id = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    replacement_teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")


class WeekdayEnum(PythonEnum):
    SATURDAY = "شنبه"
    SUNDAY = "یکشنبه"
    MONDAY = "دوشنبه"
    TUESDAY = "سه‌شنبه"
    WEDNESDAY = "چهارشنبه"
    THURSDAY = "پنجشنبه"
    FRIDAY = "جمعه"


class Day_form(Base, BaseTable):
    __tablename__ = 'days'
    day_pk_id = create_Unique_ID()
    time_sheet_fk_id = create_forenKey("employee_timesheet")
    date = Column(Date, nullable=False)
    day_of_week = Column(Enum(WeekdayEnum), nullable=False)
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=False)
    delta_time = Column(Interval, nullable=False)


class Employee_Timesheet_form(Base, BaseTable):
    __tablename__ = "employee_timesheet"
    employee_timesheet_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")


class Business_Trip_form(Base, BaseTable):
    __tablename__ = "business_trip"
    business_trip_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    destination = Column(String)
    description = Column(String)


class Teachers_Report_form(Base, BaseTable):
    __tablename__ = "teachers_report"
    teachers_report_pk_id = create_Unique_ID()
    created_by_fk_id = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    score = Column(Float)
    number_of_student = Column(Integer)
    has_cancellation = Column(Boolean, default=False)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)


## Survey Form
class survey_form(Base, BaseTable):
    __tablename__ = "forms"

    form_pk_id = create_Unique_ID()
    class_fk_id = create_forenKey("classes")
    title = Column(String, index=True)


class Questions_form(Base, BaseTable):
    __tablename__ = "question"
    question_pk_id = create_Unique_ID()
    text = Column(String)


class survey_questions_form(Base, BaseTable):
    __tablename__ = 'forms_questions'
    survey_questions = create_Unique_ID()
    form_fk_id = create_forenKey("forms")
    question_fk_id = create_forenKey("question")


class response_form(Base, BaseTable):
    __tablename__ = "response"
    response_pk_id = create_Unique_ID()
    student_fk_id = create_forenKey("student")
    question_fk_id = create_forenKey("question")
    form_fk_id = create_forenKey("forms")
    answer = Column(String)
