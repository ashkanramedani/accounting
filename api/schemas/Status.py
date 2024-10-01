from schemas.Base import *


class Status(Base_form):
    status_name: str
    status_cluster: str


class post_status_schema(Status):
    pass

    class Config:
        extra = 'ignore'


class update_status_schema(Status):
    status_pk_id: UUID

    class Config:
        extra = 'ignore'


class status_response(BaseModel):
    status_pk_id: UUID
    status_name: str
    status_cluster: str

    class Config:
        orm_mode = True
        extra = 'ignore'
