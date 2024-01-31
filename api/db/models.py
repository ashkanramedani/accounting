import datetime
import email
# from enum import unique
# from unicodedata import category
# from click import style
from typing import List, Union
from enum import Enum as PythonEnum

from sqlalchemy.sql.type_api import TypeEngine

from database import Base
from sqlalchemy import Enum, Boolean, Column, ForeignKey, Integer, String, DateTime, Table, BigInteger, Date, Time, UniqueConstraint, Index, MetaData, Float, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import expression, func
from email.policy import default
from uuid import UUID
from typing import Optional, List, Dict, Any

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL


metadata_obj = MetaData()


# __all__ = [
#     "Student",
#     "Employees",
#     "Leave_Request",
#     "Teacher_Tardy_Reports",
#     "Survey_Question",
#     "Survey",
#     "Teachers_Report",
#     "Class_Cancellation",
#     "Teacher_Replacement",
#     "Employee_Timesheet",
#     "Business_Trip",
#     "Remote_Request"]


# PK

class Student_form(Base):
    __tablename__ = "student"
    student_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)


class Class_form(Base):
    __tablename__ = "classes"
    class_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)


class Employees_signup_form(Base):
    __tablename__ = "employees"
    employees_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    job_title = Column(String, index=True)


class Leave_request_form(Base):
    __tablename__ = "leave_request"
    leave_request_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    created_by = Column(Integer, ForeignKey("employees.employee_pk_id"))
    employee_id = Column(Integer, ForeignKey("employees.employees_pk_id", ondelete='SET NULL'), nullable=False)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    Description = Column(String)



class Remote_Request_form(Base):
    __tablename__ = "remote_requests"
    remote_request_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    create_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    working_location = Column(String)
    description = Column(String)


class Teacher_tardy_reports_form(Base):
    __tablename__ = "teacher_tardy_reports"
    Teacher_tardy_reports_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    created_by = Column(Integer, ForeignKey("employees.employee_pk_id"))
    teacher_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    class_id = Column(Integer, ForeignKey("classes.class_pk_id"))
    delay = Column(Interval)


class Class_Cancellation_form(Base):
    __tablename__ = "class_cancellation"
    Class_Cancellation_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    created_date = Column(Date)
    created_by = Column(Integer, ForeignKey("employees.employee_pk_id"))
    class_id = Column(Integer, ForeignKey("classes.class_pk_id"))
    teacher_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    replacement = Column(Date)
    class_duration = Column(Interval)
    class_location = Column(String)
    description = Column(String)


class Teacher_Replacement_form(Base):
    __tablename__ = "teacher_replacement"
    teacher_replacement_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    created_by = Column(Integer, ForeignKey("employees.employee_pk_id"))
    teacher_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    replacement_teacher_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    class_id = Column(Integer, ForeignKey("classes.class_pk_id"))




class WeekdayEnum(PythonEnum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'

class Day_form(Base):
    __tablename__ = 'days'
    day_pk_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    day_of_week = Column(Enum(WeekdayEnum), nullable=False)
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=False)
    delta_time = Column(Interval, nullable=False)
    timesheet = relationship("Employee_Timesheet_form", back_populates="day")


class Employee_Timesheet_form(Base):
    __tablename__ = "employee_timesheet"
    employee_timesheet_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey('days.day_pk_id'))
    day = relationship("Day_form", back_populates="timesheet")


class Business_Trip_form(Base):
    __tablename__ = "business_trip"
    business_trip_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    destination = Column(String)
    description = Column(String)

class Teachers_Report_form(Base):
    __tablename__ = "teachers_report"
    teachers_report_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    created_by = Column(Integer, ForeignKey("employees.employee_pk_id"))
    teacher_id = Column(Integer, ForeignKey("employees.employee_pk_id"))
    ...


## Survey Form
class Survey_form(Base):
    __tablename__ = "surveys"

    survey_form_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("classes.class_pk_id"))
    title = Column(String, index=True)

class Survey_R_Questions_Bank(Base):
    __tablename__ = "survey_r_questions"

    survey_r_questions_pk_ = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey("surveys.survey_form_pk_id"))
    question_id = Column(Integer, ForeignKey("questions.question_pk_id"))


class Questions_form(Base):
    __tablename__ = "questions"

    question_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    text = Column(String)


# class Response_form(Base):
#     __tablename__ = "response"

#     response_pk__id = Column(Integer, ForeignKey("response.response_pk__id"))
#     student_id = Column(Integer, ForeignKey("student.student_pk_id"))

# class Response_R_Answer(Base):
    # __tablename__ = "response_r_answer"

    # survey_r_questions_pk_ = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    # response_id = Column(Integer, ForeignKey("response.response_pk__id"))
    # question_id = Column(Integer, ForeignKey("answers.answer_pk_id"))


# class Answer_form(Base):
#     __tablename__ = "answers"

#     answer_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
#     question_id = Column(Integer, ForeignKey("questions.question_pk_id"))
#     answer = Column(String)



 class RRR(Base):
    __tablename__ = "tbl_rrr"
    
    response_pk_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    student_fk_id = Column(Integer, ForeignKey("student.student_pk_id"))
    question_fk_id = Column(Integer, ForeignKey("questions.question_pk_id"))
    answer = Column(String)