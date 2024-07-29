from schemas.Base import *


class post_Session_Cancellation_schema(Base_form):
    session_fk_id: UUID

    class Config:
        extra = 'ignore'


class Verify_Session_Cancellation_schema(BaseModel):
    session_cancellation_pk_id: List[UUID]

    class Config:
        extra = 'ignore'


class Session_Cancellation_Response(BaseModel):
    class Config:
        extra = 'ignore'
        orm_mode = True
