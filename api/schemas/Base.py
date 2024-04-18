import uuid
from datetime import datetime, date, time, timedelta
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
    roles: List[export_role] | None

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
    day_of_birth: str | datetime = datetime.now()
    email: str | None
    mobile_number: str | None
    id_card_number: str | None
    address: str | None


class Base_response(BaseModel):
    created: export_employee
    description: str | None = None
    status: int = 0
