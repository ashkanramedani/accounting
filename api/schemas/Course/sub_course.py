from ..Base import *


class Session_signature(BaseModel):
    days_of_week: int
    starting_time: time | str
    duration: int

    class Config:
        orm_mode = True


class Sub_Course(Base_form):
    sub_course_teacher_fk_id: UUID

    sub_course_name: str

class post_sub_course_schema(Sub_Course):
    course_fk_id: UUID

    number_of_session: NonNegativeInt

    sub_course_starting_date: date
    sub_course_ending_date: date

    sub_request_threshold: NonNegativeInt = 24
    session_signature: List[Session_signature]


class update_sub_course_schema(Sub_Course):
    sub_course_pk_id: UUID


class delete_sub_course_schema(Base_form):
    course_fk_id: UUID
    sub_course_pk_id: List[UUID]


class sub_course_response(Base_form):
    sub_course_pk_id: UUID

    sub_course_name: str

    sub_course_capacity: NonNegativeInt
    sub_course_available_seat: NonNegativeInt

    created: export_employee

    teacher: export_employee
    # available_seat: int
    # Sessions: List[export_session]
    course: export_course

    class Config:
        orm_mode = True
