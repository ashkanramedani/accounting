from ..Base import *


# -------- Language ----------

class Language(Base_form):
    language_name: str


class post_language_schema(Language):
    pass


class update_language_schema(Language):
    language_pk_id: UUID


class language_response(Base_response):
    language_name: str
    language_pk_id: UUID

    class Config:
        orm_mode = True


# ------- course_type ----------


class Course_Type(Base_form):
    course_type_name: str


class post_course_type_schema(Course_Type):
    pass


class update_course_type_schema(Course_Type):
    course_type_pk_id: UUID


class course_type_response(Base_response):
    course_type_name: str
    course_type_pk_id: UUID

    class Config:
        orm_mode = True
