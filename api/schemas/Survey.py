from typing import List

from .Base import *


# ---------------------- question ----------------------
class Question(Base_form):
    text: str
    language: UUID


class post_questions_schema(Question):
    pass


class update_questions_schema(Question):
    question_pk_id: UUID


class Question_response(update_questions_schema):
    created: export_employee

    class Config:
        orm_mode = True


class export_question(BaseModel):
    question_pk_id: UUID
    text: str
    language: UUID

    class Config:
        orm_mode = True


# ---------------------- Survey_form ----------------------

class Survey(Base_form):
    sub_course_fk_id: UUID
    title: str


class post_survey_schema(Survey):
    questions: List[UUID]


class update_survey_schema(Survey):
    survey_pk_id: UUID


class survey_response(Base_response, update_survey_schema):
    course: export_course
    questions: List[export_question]

    class Config:
        orm_mode = True


class export_survey(BaseModel):
    survey_pk_id: UUID
    title: str

    class Config:
        orm_mode = True


# ---------------------- response ----------------------
class QuestionAnswer_pair(BaseModel):
    survey_fk_id: UUID
    question_fk_id: UUID
    answer: str


class Response(Base_form):
    user_fk_id: UUID
    A_Q: List[QuestionAnswer_pair]


class post_response_schema(Response):
    survey_fk_id: UUID
    pass


class update_response_schema(Base_form):
    response_pk_id: UUID
    user_fk_id: UUID
    survey_fk_id: UUID
    question: UUID
    answer: str


class response_response(Base_response):
    student: export_student
    survey: export_survey
    question: export_question
    answer: str

    class Config:
        orm_mode = True
