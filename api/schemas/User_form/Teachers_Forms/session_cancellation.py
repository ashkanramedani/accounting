from schemas.Base import *

class Session_Cancellation(Base_form):
    session_fk_id: UUID


class post_Session_Cancellation_schema(Session_Cancellation):
    pass


class update_Session_Cancellation_schema(Session_Cancellation):
    session_cancellation_pk_id: UUID


class Verify_Session_Cancellation_schema(BaseModel):
    session_cancellation_pk_id: List[UUID]
