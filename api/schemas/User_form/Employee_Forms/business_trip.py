from schemas.Base import *


class business_trip(Base_form):
    destination: str


class post_business_trip_schema(business_trip):
    user_fk_id: UUID
    start_date: datetime | str = DATETIME_NOW(2)
    end_date: datetime | str = DATETIME_NOW(1)


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID
    start: time | str
    end: time | str
    date: date | str


class business_trip_response(Base_response):
    business_trip_pk_id: UUID
    start: Optional[time] = None
    end: Optional[time] = None
    date: date | str
    destination: str
    employee: export_employee

    class Config:
        orm_mode = True


class Verify_business_trip_schema(BaseModel):
    business_trip_id: List[UUID]
