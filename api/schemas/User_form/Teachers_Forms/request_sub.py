from schemas.Base import *


class Sub_teacher(Base_form):
    session_fk_id: UUID
    sub_teacher_fk_id: UUID


class post_Sub_request_schema(Sub_teacher):
    class Config:
        extra = 'ignore'


class update_Sub_request_schema(Sub_teacher):
    sub_request_pk_id: UUID

    class Config:
        extra = 'ignore'


class Verify_Sub_request_schema(BaseModel):
    sub_request_pk_id: List[UUID]

    class Config:
        extra = 'ignore'


class Sub_request_Response(Base_response):
    sub_request_pk_id: UUID

    created: export_employee
    course: export_course
    sub_course: export_sub_course
    sessions: export_session
    main_teacher: export_employee
    sub_teacher: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True
