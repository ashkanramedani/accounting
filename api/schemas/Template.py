from schemas.Base import *


class Template(BaseModel):
    template_name: str
    data: Dict

    class Config:
        extra = 'ignore'


class post_template_schema(Template):
    template_table: str

    class Config:
        extra = 'ignore'


class update_template_schema(Template):
    template_pk_id: UUID

    class Config:
        extra = 'ignore'


class template_response(BaseModel):
    template_pk_id: UUID
    template_name: str
    template_table: str
    data: Dict

    class Config:
        extra = 'ignore'
        orm_mode = True
