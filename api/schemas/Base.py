import uuid
from datetime import timedelta
from datetime import time, date, datetime, date
from enum import Enum
from typing import Optional, List, Any, Tuple
from uuid import UUID
from pydantic import BaseModel, PositiveInt

class Sort_Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Leave_type(str, Enum):
    vacation = "vacation"
    medical = "medical"


class job_title_Enum(str, Enum):
    teacher = "teacher"
    office = "office"
    rd = "rd"
    supervisor = "supervisor"


# Base Exports
class export_role(BaseModel):
    role_pk_id: UUID
    name: str
    cluster: str

    class Config:
        orm_mode = True


class export_employee(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    # roles: List[export_role] | None

    class Config:
        orm_mode = True


class export_course(BaseModel):
    course_pk_id: UUID
    name: str
    course_time: str | datetime = datetime.now()
    duration: PositiveInt | Any
    teachers: List[export_employee]

    class Config:
        orm_mode = True


class export_student(BaseModel):
    student_pk_id: UUID
    name: str
    last_name: str

    class Config:
        orm_mode = True

class export_language(BaseModel):
    language_name: str
    # created: export_employee

    class Config:
        orm_mode = True

class export_course_type(BaseModel):
    course_type_name: str
    # created: export_employee

    class Config:
        orm_mode = True


class export_sub_course(BaseModel):
    sub_course_pk_id: UUID

    sub_course_name: str
    number_of_session: int
    sub_course_starting_date: date
    sub_course_ending_date: date

    sub_course_capacity: int
    sub_course_available_seat: int

    teacher: export_employee
    course: export_course

    class Config:
        orm_mode = True


class export_session(BaseModel):
    session_pk_id: UUID

    is_sub: bool
    session_date: date
    session_starting_time: time
    session_ending_time: time

    course: export_course
    sub_course: export_sub_course
    teacher: export_employee


class export_tag(BaseModel):
    tag_pk_id: UUID
    tag_name: str
    # created: export_employee

    class Config:
        orm_mode = True


class export_categories(BaseModel):
    category_pk_id: UUID
    category_name: str
    # created: export_employee

    class Config:
        orm_mode = True

# Base Entry
class Base_form(BaseModel):
    created_fk_by: UUID
    description: str | None = None
    status: int = 0

    visible: Optional[bool] = True
    priority: Optional[int] = 5
    can_update: Optional[bool] = True
    can_deleted: Optional[bool] = True


class Entity(BaseModel):
    name: str
    last_name: str
    day_of_birth: Optional[str] | Optional[date] = datetime.now().date()
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    id_card_number: Optional[str] = None
    address: Optional[str] = None

class Base_response(BaseModel):
    created: export_employee
    description: str | None = None
    status: int = 0
