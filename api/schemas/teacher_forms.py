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

class teacher_replacement(Base_form):
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    course_fk_id: UUID


class post_teacher_replacement_schema(teacher_replacement):
    pass


class update_teacher_replacement_schema(teacher_replacement):
    teacher_replacement_pk_id: UUID


class teacher_replacement_response(Base_response, update_teacher_replacement_schema):
    main_teacher: export_employee
    replacement_teacher: export_employee
    course: export_course

    class Config:
        orm_mode = True
