from schemas.Base import *


class post_Session_Cancellation_schema(Base_form):
    session_fk_id: UUID

    class Config:
        extra = 'ignore'


class Verify_Session_Cancellation_schema(BaseModel):
    session_cancellation_pk_id: List[UUID]

    class Config:
        extra = 'ignore'


class Session_Cancellation_Response(Base_response):
    session_cancellation_pk_id: UUID
    course: export_course
    sub_course: export_sub_course
    session: export_session

    class Config:
        extra = 'ignore'
        orm_mode = True
