from .Base import *


# ---------------------- teacher_tardy_reports ----------------------
class teacher_tardy_reports(Base_form):
    teacher_fk_id: UUID
    course_fk_id: UUID
    sub_course_fk_id: UUID
    delay: PositiveInt


class post_teacher_tardy_reports_schema(teacher_tardy_reports):
    pass


class update_teacher_tardy_reports_schema(teacher_tardy_reports):
    teacher_tardy_reports_pk_id: UUID


class teacher_tardy_reports_response(Base_response):
    teacher_tardy_reports_pk_id: UUID
    delay: PositiveInt
    teacher: export_employee
    course: export_course
    sub_course: export_sub_course


    class Config:
        orm_mode = True


# ---------------------- teacher_replacement ----------------------
class Sub_teacher(Base_form):
    main_teacher_fk_id: UUID
    sub_teacher_fk_id: UUID
    session_fk_id: UUID

class post_Sub_request_schema(Sub_teacher):
    pass

class update_Sub_request_schema(Sub_teacher):
    sub_request_pk_id: UUID

class Verify_Sub_request_schema(BaseModel):
    sub_request_pk_id: List[UUID]

class Sub_teacher_Response(BaseModel):
    pass

    class Config:
        orm_mode = True

class subcourse_teacher_replacement(BaseModel):
    replacement_date: datetime | str
    subcourse_fk_id: UUID
    sub_teacher_fk_id: UUID


