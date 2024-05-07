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
class Update_Relation(BaseModel):
    old_id: UUID | None | str
    new_id: UUID | None | str


class course(Base_form):
    course_name: str

    starting_date: date
    ending_date: date
    course_capacity: int

    course_language: UUID
    course_type: UUID

    tags: List[Update_Relation]
    categories: List[Update_Relation]

    course_code: str
    course_image: str = ""

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

    language: export_language
    type: export_course_type

    teachers: List[export_employee] | List[UUID] = None
    course_signature: List[Session_signature] = []
    available_seat: int = None

    tags: List[export_tag] | None
    categories: Optional[List[export_categories]]

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


class sub_course_response(BaseModel):
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


class language_response(update_language_schema):
    created: export_employee

    class Config:
        orm_mode = True


# ------- course_type ----------


class Course_Type(Base_form):
    course_type_name: str


class post_course_type_schema(Course_Type):
    pass


class update_course_type_schema(Course_Type):
    course_type_pk_id: UUID


class course_type_response(update_course_type_schema):
    created: export_employee

    class Config:
        orm_mode = True

# ----- Course cancellation
class course_cancellation(Base_form):
    course_fk_id: UUID
    teacher_fk_id: UUID
    replacement_date: datetime = datetime.now()
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

