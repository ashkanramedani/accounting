from schemas.Base import *


class leave_request(Base_form):
    leave_type: Leave_type = "vacation"


class post_leave_request_schema(leave_request):
    user_fk_id: UUID
    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(1)

class update_leave_request_schema(leave_request):
    leave_request_pk_id: UUID
    start: str | time
    end: str | time
    date: str | date


class Verify_leave_request_schema(BaseModel):
    leave_request_id: List[UUID]


class leave_request_response(Base_response):
    leave_request_pk_id: UUID
    employee: export_employee

    start: Optional[time] = None
    end: Optional[time] = None
    date: str | date
    duration: NonNegativeInt

    leave_type: str

    class Config:
        orm_mode = True
