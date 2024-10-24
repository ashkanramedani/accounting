from .Base import *


# -------------------------------   Tag  -------------------------------
class Tag(Base_form):
    tag_name: str
    tag_cluster: str = "Main"


class post_tag_schema(Tag):
    pass


class update_tag_schema(Tag):
    tag_pk_id: UUID


class tag_response(update_tag_schema):
    created: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True


# -------------------   Categories  -------------------
class Category(Base_form):
    category_name: str
    category_cluster: str = "Main"


class post_category_schema(Category):
    pass


class update_category_schema(Category):
    category_pk_id: UUID


class category_response(update_category_schema):
    created: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True
