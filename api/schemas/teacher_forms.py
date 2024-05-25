from .Base import *


# ---------------------- teacher_tardy_reports ----------------------
class teacher_tardy_reports(Base_form):
    teacher_fk_id: UUID
    course_fk_id: UUID
    delay: PositiveInt


class post_teacher_tardy_reports_schema(teacher_tardy_reports):
    pass


class update_teacher_tardy_reports_schema(teacher_tardy_reports):
    teacher_tardy_reports_pk_id: UUID


class teacher_tardy_reports_response(Base_response, update_teacher_tardy_reports_schema):
    teacher: export_employee
    course: export_course

    class Config:
        orm_mode = True


# ---------------------- teacher_replacement ----------------------
class session_teacher_replacement(BaseModel):
    sub_course_fk_id: UUID
    sessions: List[UUID]
    sub_teacher_fk_id: UUID


class subcourse_teacher_replacement(BaseModel):
    replacement_date: date | str
    subcourse_fk_id: UUID
    sub_teacher_fk_id: UUID


# ---------------------- course cancellation ----------------------
class course_cancellation(BaseModel):
    course_pk_id: UUID


class sub_course_cancellation(BaseModel):
    course_fk_id: UUID
    sub_course_pk_id: List[UUID]


class session_cancellation(BaseModel):
    sub_course_fk_id: UUID
    session_pk_id: List[UUID]
