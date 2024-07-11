from schemas.Base import *


class remote_request(Base_form):
    user_fk_id: UUID
    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(1)
    working_location: str = ""


class post_remote_request_schema(remote_request):
    pass


class update_remote_request_schema(remote_request):
    remote_request_pk_id: UUID


class Verify_remote_request_schema(BaseModel):
    remote_request_id: List[UUID]


class remote_request_response(Base_response):
    remote_request_pk_id: UUID

    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(2)
    working_location: str = ""

    employee: export_employee

    class Config:
        orm_mode = True
