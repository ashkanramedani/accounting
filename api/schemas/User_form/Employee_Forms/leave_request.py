from schemas.Base import *


class leave_request(Base_form):
    user_fk_id: UUID
    leave_type: Leave_type = "vacation"
    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(1)


class post_leave_request_schema(leave_request):
    pass


class update_leave_request_schema(BaseModel):
    leave_request_pk_id: UUID

    leave_type: Leave_type = "vacation"
    start_time: str | time = NOW().time()
    end_time: str | time = NOW(2).time()


class Verify_leave_request_schema(BaseModel):
    leave_request_id: List[UUID]


class leave_request_response(Base_response):
    leave_request_pk_id: UUID
    employee: export_employee

    start_date: time | None
    end_date: time | None
    date: datetime
    duration: int

    leave_type: str

    class Config:
        orm_mode = True
