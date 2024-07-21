from schemas.Base import *


class leave_request(Base_form):
    leave_type: Leave_type = "vacation"


class post_leave_request_schema(leave_request):
    user_fk_id: UUID
    start_date: datetime | str = DATETIME_NOW()
    end_date: datetime | str = DATETIME_NOW(1)


class update_leave_request_schema(leave_request):
    leave_request_pk_id: UUID
    start: time | str
    end: time | str
    date: date | str


class Verify_leave_request_schema(BaseModel):
    leave_request_id: List[UUID]


class leave_request_response(Base_response):
    leave_request_pk_id: UUID
    employee: export_employee

    start: Optional[time] = None
    end: Optional[time] = None
    date: date | str
    duration: NonNegativeInt

    leave_type: str

    class Config:
        orm_mode = True
