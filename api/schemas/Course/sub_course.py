from ..Base import *


class Session_signature(BaseModel):
    days_of_week: int
    starting_time: time | str
    duration: int

    class Config:
        orm_mode = True


class post_sub_course_schema(Base_form):
    course_fk_id: UUID
    sub_course_teacher_fk_id: UUID

    sub_course_name: str
    number_of_session: int

    sub_request_threshold: int = 24
    sub_course_starting_date: date
    sub_course_ending_date: date

    session_signature: List[Session_signature]


class update_sub_course_schema(Base_form):
    sub_course_pk_id: UUID
    sub_course_teacher_fk_id: UUID

    sub_course_name: str
    number_of_session: int
    sub_course_starting_date: date
    sub_course_ending_date: date


class delete_sub_course_schema(Base_form):
    course_fk_id: UUID
    sub_course_pk_id: List[UUID]


class sub_course_response(Base_response):
    sub_course_pk_id: UUID

    sub_course_name: str
    number_of_session: NonNegativeInt
    sub_course_capacity: NonNegativeInt
    sub_course_available_seat: NonNegativeInt

    sub_course_starting_date: date
    sub_course_ending_date: date
    created: export_employee

    teacher: export_employee
    # available_seat: int
    # Sessions: List[export_session]
    course: export_course

    class Config:
        orm_mode = True
