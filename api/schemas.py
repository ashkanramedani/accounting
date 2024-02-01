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


# Employees Base Model
class Employee_post_schema(BaseModel):
    name: str
    last_name: str
    job_title: str


# Leave Requests Base Model
class get_leave_request_schema(BaseModel):
    form_id: UUID | None = None


class post_leave_request_schema(BaseModel):
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


class delete_leave_request_schema(BaseModel):
    form_id: UUID


class update_leave_request_schema(BaseModel):
    leave_request_id: UUID
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


# student
class get_student_schema(BaseModel):
    student_id: UUID | None = None


class post_student_schema(BaseModel):
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


class delete_student_schema(BaseModel):
    student_id: UUID | None = None


class update_student_schema(BaseModel):
    student_pk_id: UUID
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


# Class Base Model
class get_class_schema(BaseModel):
    class_pk_id: UUID | None = None


class post_class_schema(BaseModel):
    starting_time: time
    duration = timedelta
    class_date: date


class delete_class_schema(BaseModel):
    class_pk_id: UUID


class update_class_schema(BaseModel):
    class_pk_id: UUID
    starting_time: time
    duration = timedelta
    class_date: date


# Remote Request

class get_remote_request_schema(BaseModel):
    remote_request_pk_id: UUID | None = None


class post_remote_Request_schema(BaseModel):
    employee_fk_id: UUID
    create_date: date
    start_date: date
    end_date: date
    working_location: str
    description: str


class delete_Remote_Request_schema(BaseModel):
    remote_request_pk_id: UUID


class update_remote_Request_schema(BaseModel):
    remote_request_pk_id: UUID
    employee_fk_id: UUID
    create_date: date
    start_date: date
    end_date: date
    working_location: str
    description: str


# teacher tardy reports
class get_teacher_tardy_reports_schema(BaseModel):
    Teacher_tardy_reports_pk_id: UUID | None = None


class post_teacher_tardy_reports_schema(BaseModel):
    created_fk_by: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


class delete_teacher_tardy_reports_schema(BaseModel):
    Teacher_tardy_reports_pk_id: UUID


class update_teacher_tardy_reports_schema(BaseModel):
    Teacher_tardy_reports_pk_id: UUID
    created_fk_by: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


# class cancellation
class get_class_cancellation_schema(BaseModel):
    class_cancellation_pk_id: UUID | None = None


class post_cass_cancellation_schema(BaseModel):
    created_date: date
    created_fk_by: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


class delete_class_cancellation_schema(BaseModel):
    class_cancellation_pk_id: UUID


class update_class_cancellation_schema(BaseModel):
    class_cancellation_pk_id: UUID
    created_date: date
    created_fk_by: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


# Teacher Replacement
class get_teacher_replacement_schema(BaseModel):
    teacher_replacement_pk_id: UUID | None = None


class post_teacher_replacement_schema(BaseModel):
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


class delete_teacher_replacement_schema(BaseModel):
    teacher_replacement_pk_id: UUID


class update_teacher_replacement_schema(BaseModel):
    teacher_replacement_pk_id: UUID
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


# Business Trip Base Model
class get_business_trip_schema(BaseModel):
    business_trip_pk_id: UUID | None = None


class post_business_trip_schema(BaseModel):
    employee_fk_id: UUID
    destination: str
    description: str


class delete_business_trip_schema(BaseModel):
    business_trip_pk_id: UUID


class update_business_trip_schema(BaseModel):
    business_trip_pk_id: UUID
    employee_fk_id: UUID
    destination: str
    description: str


# DAY Base Model
class get_day_schema(BaseModel):
    day_pk_id: UUID | None = None


class post_day_schema(BaseModel):
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta


class delete_day_schema(BaseModel):
    day_pk_id: UUID


class update_day_schema(BaseModel):
    day_pk_id: UUID
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta

# MISSING CRUD
"""
Question_Bank
Survey
Response
--------
time_sheet

"""