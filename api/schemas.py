from datetime import datetime, time, timedelta, date
from uuid import UUID
from typing import List
from pydantic import BaseModel, UUID4
from enum import Enum


class WeekdayEnum(str, Enum):
    SATURDAY = "شنبه"
    SUNDAY = "یکشنبه"
    MONDAY = "دوشنبه"
    TUESDAY = "سهشنبه"
    WEDNESDAY = "چهارشنبه"
    THURSDAY = "پنجشنبه"
    FRIDAY = "جمعه"

class job_title_Enum(str, Enum):
    teacher = "teacher"
    office = "office"

# Employees Base Model

class post_employee_schema(BaseModel):
    name: str
    last_name: str
    job_title: job_title_Enum


class update_employee_schema(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    job_title: str


# Leave requests Base Model

class post_leave_request_schema(BaseModel):
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


class update_leave_request_schema(BaseModel):
    leave_request_id: UUID
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


# student

class post_student_schema(BaseModel):
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


class update_student_schema(BaseModel):
    student_pk_id: UUID
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


# Class Base Model

class post_class_schema(BaseModel):
    starting_time: time
    duration = timedelta
    class_date: date


class update_class_schema(BaseModel):
    class_pk_id: UUID
    starting_time: time
    duration = timedelta
    class_date: date


# Remote request


class post_remote_request_schema(BaseModel):
    employee_fk_id: UUID
    start_date: date
    end_date: date
    working_location: str
    description: str


class update_remote_request_schema(BaseModel):
    remote_request_pk_id: UUID
    employee_fk_id: UUID
    start_date: date
    end_date: date
    working_location: str
    description: str


# teacher tardy reports

class post_teacher_tardy_reports_schema(BaseModel):
    create_by_fk_id: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


class update_teacher_tardy_reports_schema(BaseModel):
    teacher_tardy_reports_pk_id: UUID
    create_by_fk_id: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


# class cancellation

class post_class_cancellation_schema(BaseModel):
    create_by_fk_id: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


class update_class_cancellation_schema(BaseModel):
    class_cancellation_pk_id: UUID
    create_by_fk_id: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


# Teacher Replacement

class post_teacher_replacement_schema(BaseModel):
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


class update_teacher_replacement_schema(BaseModel):
    teacher_replacement_pk_id: UUID
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


# Business Trip Base Model

class post_business_trip_schema(BaseModel):
    employee_fk_id: UUID
    destination: str
    description: str


class update_business_trip_schema(BaseModel):
    business_trip_pk_id: UUID
    employee_fk_id: UUID
    destination: str
    description: str


# DAY Base Model

class post_day_schema(BaseModel):
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta


class update_day_schema(BaseModel):
    day_pk_id: UUID
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta


class post_questions_schema(BaseModel):
    text: str

class update_questions_schema(BaseModel):
    question_pk_id: UUID
    text: str



class post_survey_schema(BaseModel):
    class_fk_id: UUID
    questions: List[UUID]
    title: str

class update_survey_schema(BaseModel):
    form_pk_id: UUID
    class_fk_id: UUID
    questions: List[UUID]
    title: str


class update_survey_question_schema(BaseModel):
    form_pk_id: UUID
    questions_fk_id: UUID
    new_question_fk_id: UUID


class post_response_schema(BaseModel):
    student_fk_id: UUID
    question_fk_id: UUID
    form_fk_id: UUID
    answer: str


class update_response_schema(BaseModel):
    response_pk_id: UUID
    student_fk_id: UUID
    question_fk_id: UUID
    form_fk_id: UUID
    answer: str



# MISSING CRUD
"""

--------
time_sheet

"""
