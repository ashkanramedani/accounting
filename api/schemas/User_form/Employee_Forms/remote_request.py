from schemas.Base import *


class remote_request(Base_form):
    working_location: str = ""


class post_remote_request_schema(remote_request):
    user_fk_id: UUID
    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(1)


class update_remote_request_schema(remote_request):
    remote_request_pk_id: UUID
    start: str | time
    end: str | time
    date: str | date


class Verify_remote_request_schema(BaseModel):
    remote_request_id: List[UUID]


class remote_request_response(Base_response):
    remote_request_pk_id: UUID

    start: Optional[time] = None
    end: Optional[time] = None
    date: str | date
    working_location: str = ""

    employee: export_employee

    class Config:
        orm_mode = True
