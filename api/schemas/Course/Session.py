from ..Base import *

class Session(Base_form):
    course_fk_id: UUID
    sub_course_fk_id: UUID
    session_teacher_fk_id: UUID

    session_date: date
    session_starting_time: time
    session_duration: NonNegativeInt
    sub_request_threshold: NonNegativeInt = 24  # Hour

    # Not Necceccery
    # session_ending_time: time
    # is_sub: bool = False
    # days_of_week: int


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
