from ..Base import *


class Role(Base_form):
    name: str
    cluster: str


class post_role_schema(Role):
    pass


class update_role_schema(Role):
    role_pk_id: UUID


class role_response(BaseModel):
    role_pk_id: UUID
    name: str
    cluster: str
    status: str
    description: str
    created: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True
