from .Base import *
from .Entity import *


class leave_request(Base_form):
    employee_fk_id: UUID
    leave_type: Leave_type = "vacation"
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now() + timedelta(days=1)


class post_leave_request_schema(leave_request):
    pass


class update_leave_request_schema(leave_request):
    leave_request_pk_id: UUID


class leave_request_response(Base_form, Base_response):
    leave_request_pk_id: UUID
    employee: export_employee

    start_date: time | None
    end_date: time | None
    date: datetime | None
    duration: int

    leave_type: str

    class Config:
        orm_mode = True


# ---------------------- remote_request ----------------------
class remote_request(Base_form):
    employee_fk_id: UUID
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()
    working_location: str = ""


class post_remote_request_schema(remote_request):
    pass


class update_remote_request_schema(remote_request):
    remote_request_pk_id: UUID


class remote_request_response(update_remote_request_schema, Base_response):
    employee: export_employee

    class Config:
        orm_mode = True


# ---------------------- business_trip ----------------------
class business_trip(Base_form):
    employee_fk_id: UUID
    destination: str
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()


class post_business_trip_schema(business_trip):
    pass


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID


class business_trip_response(update_business_trip_schema, Base_response):
    employee: export_employee

    class Config:
        orm_mode = True
