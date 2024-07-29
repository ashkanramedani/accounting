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


class Sub_teacher_Response(BaseModel):
    class Config:
        extra = 'ignore'
        orm_mode = True
