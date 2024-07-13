from schemas.Base import *

class business_trip(Base_form):
    destination: str


class post_business_trip_schema(business_trip):
    user_fk_id: UUID
    start_date: str | datetime = NOW(2)
    end_date: str | datetime = NOW(1)


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID
    start: str | time
    end: str | time
    date: str | date



class business_trip_response(Base_response):
    business_trip_pk_id: UUID
    start: Optional[time] = None
    end: Optional[time] = None
    date: str | date
    destination: str
    employee: export_employee

    class Config:
        orm_mode = True


class Verify_business_trip_schema(BaseModel):
    business_trip_id: List[UUID]
