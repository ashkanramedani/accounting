import schemas as sch
import db.models as dbm

from .Extra import *
from uuid import UUID
from lib import logger

from typing import List
from sqlalchemy.orm import Session


# response
def get_response(db: Session, response_id):
    try:
        return 200, db.query(dbm.Response_form).filter_by(response_pk_id=response_id, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_response(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Response_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


def post_response(db: Session, Form: sch.post_response_schema):
    try:
        if not db.query(dbm.User_form).filter_by(user_pk_id=Form.student_fk_id, deleted=False).first():
            return 400, "Bad Request: Student not found"

        if not db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_fk_id, deleted=False).first():
            return 400, "Bad Request: Survey not found"

        data = Form.dict()
        question_answer_pair = data.pop("answer")
        all_questions: List[UUID] = [question["question_pk_id"] for question in db.query(dbm.Question_form).filter_by(deleted=False).all()]

        Responses = []
        for Q, A in question_answer_pair:
            if Q not in all_questions:
                return 400, "Bad Request: Question not found"
            Responses.append(dbm.Response_form(student_fk_id=student_fk_id, question_fk_id=question_fk_id, survey_fk_id=survey_fk_id, answer=answer))  # type: ignore[call-arg]

        db.add_all(Responses)
        db.commit()
        return 200, "response Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_response(db: Session, response_id):
    try:
        record = db.query(dbm.Response_form).filter_by(response_pk_id=response_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_response(db: Session, Form: sch.update_response_schema):
    try:
        record = db.query(dbm.Response_form).filter_by(response_pk_id=Form.response_pk_id, deleted=False)
        if not record.first():
            return 400, "Bad request: Record not found"

        if not db.query(dbm.User_form).filter_by(user_pk_id=Form.student_fk_id, deleted=False).first():
            return 400, "Bad Request: Student not found"

        if not db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_fk_id, deleted=False).first():
            return 400, "Bad Request: Survey not found"

        if not db.query(dbm.Question_form).filter_by(question_pk_id=Form.question, deleted=False).first():
            return 400, "Bad Request: Question not found"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
