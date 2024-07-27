from datetime import time, date, datetime, timedelta
from enum import Enum
from typing import Optional, Any, List
from uuid import UUID

from faker import Faker
from pydantic import BaseModel, EmailStr, NonNegativeInt, PositiveInt

SUCCESS_STATUS: List[PositiveInt] = [200, 201]
identity: Faker = Faker()


def DATETIME_NOW(Off_Set: int = 0) -> datetime:
    return datetime.now() + timedelta(days=Off_Set)


def DATE_NOW(Off_Set: int = 0) -> date:
    return (datetime.now() + timedelta(days=Off_Set)).date()


def TIME_NOW(Off_Set: int = 0) -> time:
    return (datetime.now() + timedelta(hours=Off_Set)).time()


class CanUpdateStatus(str, Enum):
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"


class ValidStatus(str, Enum):
    submitted = "submitted"
    approved = "approved"
    canceled = "canceled"
    rejected = "rejected"
    deleted = "deleted"


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
    user_pk_id: UUID
    name: str
    last_name: str

    # roles: List[export_role] | None

    class Config:
        orm_mode = True


class export_course(BaseModel):
    course_pk_id: UUID
    course_name: str
    starting_date: date
    ending_date: date
    course_level: str

    class Config:
        orm_mode = True


class export_student(BaseModel):
    user_pk_id: UUID
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
    number_of_session: NonNegativeInt
    sub_course_starting_date: date
    sub_course_ending_date: date

    sub_course_capacity: NonNegativeInt
    sub_course_available_seat: NonNegativeInt

    teacher: export_employee

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
    created_fk_by: UUID = "00000000-0000-4b94-8e27-44833c2b940f"
    description: str | None = None

    visible: Optional[bool] = True
    priority: Optional[int] = 5
    can_update: Optional[bool] = True
    can_deleted: Optional[bool] = True


class user_dropdown(BaseModel):
    name: str
    last_name: str
    user_pk_id: UUID

    class Config:
        orm_mode = True


class Entity(BaseModel):
    name: str = identity.first_name()
    last_name: str = identity.last_name()
    email: EmailStr = identity.email()

    level: Optional[str] = ""
    address: Optional[str] = None
    id_card_number: Optional[str] = ""
    mobile_number: Optional[str] = identity.phone_number()
    day_of_birth: Optional[date | str] = identity.date_this_century()


class Entity_Response(BaseModel):
    name: str
    last_name: str
    email: str

    level: Optional[str] = ""
    address: Optional[str] = None
    id_card_number: Optional[str] = ""
    mobile_number: Optional[str]
    day_of_birth: Optional[date | str]

    class Config:
        orm_mode = True


class Base_response(BaseModel):
    created: Optional[export_employee] = {}
    description: str | None = None
    status: ValidStatus = "submitted"
    priority: int

    class Config:
        orm_mode = True


class Base_record_add(BaseModel):
    id: UUID | str | None
    Warning: Optional[str] = None


class Update_Relation(BaseModel):
    old_id: UUID | str = ""
    new_id: UUID | str = ""

    class Config:
        orm_mode = True


class Route_Result(BaseModel):
    route: str
    status: int
    body: Any


class Employee_salary(Entity):
    user_pk_id: UUID

    class Config:
        orm_mode = True
