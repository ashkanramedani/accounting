import random

from .Base import *
from .Entity import *


class Session_signature(BaseModel):
    days_of_week: int
    starting_time: time
    duration: int

    class Config:
        orm_mode = True


# ---------------------- class ----------------------
class course(Base_form):
    course_pk_id: UUID
    course_name: str

    starting_date: date
    ending_date: date
    course_capacity: int

    course_language: UUID
    course_type: UUID

    tags: List[UUID] = []
    categories: List[UUID] = []
    course_code: str
    course_image: str = ""

    course_level: str
    package_discount: float


class post_course_schema(course):
    pass


class update_course_schema(course):
    course_pk_id: UUID


class course_response(update_course_schema):
    teachers: List[export_employee] | List[UUID]
    course_number_of_session: int = 0
    course_signature: List[Session_signature] = []
    available_seat: int
    total_seat: int

    class Config:
        orm_mode = True


# ________ Session

class Session(BaseModel):
    course_fk_id: UUID
    created_fk_by: UUID
    sub_course_fk_id: UUID
    session_teacher_fk_id: UUID

    is_sub: bool = False
    session_date: date
    session_starting_time: time
    session_ending_time: time
    session_duration: int
    days_of_week: int


class post_session_schema(Session):
    pass


class update_session_schema(Session):
    session_pk_id: UUID


class session_response(update_session_schema):
    created: export_employee
    teacher: export_employee
    sub_teacher: export_employee | None

    class Config:
        orm_mode = True

class export_session(session_response):
    pass

    class Config:
        orm_mode = True

# ------- SubCourse - --
class SubCourse(BaseModel):
    course_fk_id: UUID
    created_fk_by: UUID
    sub_course_teacher_fk_id: UUID

    sub_course_name: str
    number_of_session: int

    sub_course_starting_date: date
    sub_course_ending_date: date

    session_signature: List[Session_signature]


class post_sub_course_schema(SubCourse):
    pass


class update_sub_course_schema(SubCourse):
    sub_course_pk_id: UUID


class sub_course_response(update_sub_course_schema):
    teacher: export_employee
    available_seat: int
    Sessions: List[export_session]

    class Config:
        orm_mode = True


# ----- Course cancellation
class course_cancellation(Base_form):
    course_fk_id: UUID
    teacher_fk_id: UUID
    replacement_date: str | datetime = datetime.now()
    course_duration: PositiveInt
    course_location: str


class post_course_cancellation_schema(course_cancellation):
    pass


class update_course_cancellation_schema(course_cancellation):
    course_cancellation_pk_id: UUID


class course_cancellation_response(Base_response, update_course_cancellation_schema):
    teacher: export_employee
    course: export_course

    class Config:
        orm_mode = True