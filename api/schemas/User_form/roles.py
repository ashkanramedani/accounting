from ..Base import *


class Role(Base_form):
    name: str
    cluster: str


class post_role_schema(Role):
    pass


class update_role_schema(Role):
    role_pk_id: UUID


class role_response(Base_response):
    role_pk_id: UUID
    name: str
    cluster: str

    class Config:
        extra = 'ignore'
        orm_mode = True
