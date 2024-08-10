from schemas.Base import *


class Template(Base_form):
    template_name: str
    data: Dict

    class Config:
        extra = 'ignore'
        orm_mode = True

class post_template_schema(Template):
    template_table: str

    class Config:
        extra = 'ignore'
        orm_mode = True

class update_template_schema(Template):
    template_pk_id: UUID

    class Config:
        extra = 'ignore'
        orm_mode = True

class template_response(Base_response):
    template_pk_id: UUID
    template_name: str
    template_table: str
    data: Dict

    class Config:
        extra = 'ignore'
        orm_mode = True
