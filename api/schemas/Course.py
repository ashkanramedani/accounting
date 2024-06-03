import random

from .Base import *
from .Entity import *


class Session_signature(BaseModel):
    days_of_week: int
    starting_time: time | str
    duration: int

    class Config:
        orm_mode = True


# ---------------------- class ----------------------
class course(Base_form):
    course_name: str

    starting_date: date
    ending_date: date
    course_capacity: int

    course_language: UUID = "7f371975-e397-4fc5-b719-75e3978fc547"
    course_type: UUID = "7f485938-f59f-401f-8859-38f59f201f3e"

    course_code: str
    course_image: str = ""

    tags: Optional[List[Update_Relation]] = []
    categories: Optional[List[Update_Relation]] = []

    course_level: str
    package_discount: float


class post_course_schema(course):
    pass


class update_course_schema(course):
    course_pk_id: UUID


class course_response(Base_response):
    course_pk_id: UUID

    course_name: str
    package_discount: float
    course_image: str
    course_capacity: int
    course_level: str
    course_code: str

    starting_date: date
    ending_date: date

    teachers: List[export_employee] | List[UUID] = None
    course_signature: List[Session_signature] = []
    available_seat: int = None

    tags: List[export_tag] = []
    categories: List[export_categories] = []
    language: export_language
    type: export_course_type

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


class session_response(Base_response):
    session_pk_id: UUID
    course_fk_id: UUID

    is_sub: bool
    session_date: date
    session_starting_time: time
    session_ending_time: time
    session_duration: int
    days_of_week: int
    course: export_course
    sub_course: export_sub_course
    teacher: export_employee

    class Config:
        orm_mode = True


class export_session(BaseModel):
    session_pk_id: UUID
    session_starting_time: time
    session_ending_time: time
    session_duration: int
    days_of_week: int
    teacher: export_employee

    class Config:
        orm_mode = True


# ------- SubCourse - --
class SubCourse(Base_form):
    course_fk_id: UUID
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


class delete_sub_course_schema(Base_form):
    course_fk_id: UUID
    sub_course_pk_id: List[UUID]


class sub_course_response(Base_response):
    sub_course_pk_id: UUID
    course_fk_id: UUID
    sub_course_teacher_fk_id: UUID

    sub_course_name: str
    number_of_session: int

    sub_course_starting_date: date
    sub_course_ending_date: date
    created: export_employee

    # teacher: export_employee
    # available_seat: int
    # Sessions: List[export_session]

    class Config:
        orm_mode = True


# -------- Language ----------

class Language(Base_form):
    language_name: str


class post_language_schema(Language):
    pass


class update_language_schema(Language):
    language_pk_id: UUID


class language_response(Base_response):
    language_name: str
    language_pk_id: UUID

    class Config:
        orm_mode = True


# ------- course_type ----------


class Course_Type(Base_form):
    course_type_name: str


class post_course_type_schema(Course_Type):
    pass


class update_course_type_schema(Course_Type):
    course_type_pk_id: UUID


class course_type_response(Base_response):
    course_type_name: str
    course_type_pk_id: UUID

    class Config:
        orm_mode = True

# ---------------------- course cancellation ---------------------
