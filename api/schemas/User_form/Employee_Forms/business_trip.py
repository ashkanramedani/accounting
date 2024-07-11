from schemas.Base import *

class business_trip(Base_form):
    user_fk_id: UUID
    destination: str
    start_date: str | datetime = NOW(2)
    end_date: str | datetime = NOW(1)


class post_business_trip_schema(business_trip):
    pass


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID


class business_trip_response(Base_response):
    business_trip_pk_id: UUID
    destination: str
    start_date: str | datetime = NOW()
    end_date: str | datetime = NOW(2)
    employee: export_employee

    class Config:
        orm_mode = True


class Verify_business_trip_schema(BaseModel):
    business_trip_id: List[UUID]
