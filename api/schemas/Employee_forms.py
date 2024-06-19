from datetime import timedelta
from typing import List

from .Base import *
from .Entity import *


class leave_request(Base_form):
    user_fk_id: UUID
    leave_type: Leave_type = "vacation"
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now() + timedelta(days=1)


class post_leave_request_schema(leave_request):
    pass


class update_leave_request_schema(BaseModel):
    leave_request_pk_id: UUID

    leave_type: Leave_type = "vacation"
    start_time: str | time = datetime.now().time()
    end_time: str | time = (datetime.now() + timedelta(hours=3)).time()


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


# ---------------------- remote_request ----------------------
class remote_request(Base_form):
    user_fk_id: UUID
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()
    working_location: str = ""


class post_remote_request_schema(remote_request):
    pass


class update_remote_request_schema(remote_request):
    remote_request_pk_id: UUID


class Verify_remote_request_schema(BaseModel):
    remote_request_id: List[UUID]


class remote_request_response(Base_response):
    remote_request_pk_id: UUID

    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()
    working_location: str = ""

    employee: export_employee

    class Config:
        orm_mode = True


# ---------------------- business_trip ----------------------
class business_trip(Base_form):
    user_fk_id: UUID
    destination: str
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()


class post_business_trip_schema(business_trip):
    pass


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID


class business_trip_response(Base_response):
    business_trip_pk_id: UUID
    destination: str
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()
    employee: export_employee

    class Config:
        orm_mode = True


class Verify_business_trip_schema(BaseModel):
    business_trip_id: List[UUID]
