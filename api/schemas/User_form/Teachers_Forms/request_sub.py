from schemas.Base import *


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
