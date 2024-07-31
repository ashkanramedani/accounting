from schemas.Base import *


class teacher_tardy_reports(Base_form):
    delay: PositiveInt

    class Config:
        extra = 'ignore'


class post_teacher_tardy_reports_schema(teacher_tardy_reports):
    session_fk_id: UUID

    class Config:
        extra = 'ignore'


class update_teacher_tardy_reports_schema(teacher_tardy_reports):
    teacher_tardy_report_pk_id: UUID

    class Config:
        extra = 'ignore'


class Verify_teacher_tardy_reports_schema(BaseModel):
    teacher_tardy_report_pk_id: List[UUID]

    class Config:
        extra = 'ignore'


class teacher_tardy_reports_response(Base_response):
    teacher_tardy_report_pk_id: UUID
    delay: PositiveInt

    teacher: export_employee
    course: export_course
    sub_course: export_sub_course
    session: export_session

    class Config:
        extra = 'ignore'
        orm_mode = True
