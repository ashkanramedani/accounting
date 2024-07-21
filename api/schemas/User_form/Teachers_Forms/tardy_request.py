from schemas.Base import *


class teacher_tardy_reports(Base_form):
    teacher_fk_id: UUID
    course_fk_id: UUID
    sub_course_fk_id: UUID
    delay: PositiveInt


class post_teacher_tardy_reports_schema(teacher_tardy_reports):
    pass


class update_teacher_tardy_reports_schema(teacher_tardy_reports):
    teacher_tardy_report_pk_id: UUID


class teacher_tardy_reports_response(Base_response):
    teacher_tardy_report_pk_id: UUID
    delay: PositiveInt
    teacher: export_employee
    course: export_course
    sub_course: export_sub_course

    class Config:
        orm_mode = True
