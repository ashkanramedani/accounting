from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from .Extra import *




# question
def get_question(db: Session, question_id):
    try:
        return 200, db.query(dbm.Questions_form).filter_by(question_pk_id=question_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_question(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, db.query(dbm.Questions_form).filter_by(deleted=False).offset((page - 1) * limit).limit(limit).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_question(db: Session, Form: sch.post_questions_schema):
    try:
        OBJ = dbm.Questions_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_question(db: Session, question_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(question_id_pk_id=question_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_question(db: Session, Form: sch.update_questions_schema):
    try:
        record = db.query(dbm.Questions_form).filter_by(question_pk_id=Form.question_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


# survey
def get_survey(db: Session, survey_id):
    try:
        return 200, db.query(dbm.Survey_form).filter_by(survey_pk_id=survey_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_survey(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Survey_form, page, limit, order)

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_survey(db: Session, Form: sch.post_survey_schema):
    try:
        if not class_exist(db, Form.class_fk_id):
            return 400, "Bad Request"

        data = Form.dict()
        questions: List[UUID] = data.pop("questions")

        OBJ = dbm.Survey_form(**data)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if not questions:
            return 200, "Empty survey added"

        question_ID: List[UUID] = [ID.question_pk_id for ID in db.query(dbm.Questions_form).filter_by(deleted=False).all()]

        for q_id in questions:
            if q_id not in question_ID:
                return 400, "Bad Request"
            OBJ.questions.append(db.query(dbm.Questions_form).filter_by(question_pk_id=q_id, deleted=False).first())
        db.commit()
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.Survey_form).filter_by(survey_id_pk_id=survey_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True

        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_survey(db: Session, Form: sch.update_survey_schema):
    try:
        record = db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not class_exist(db, Form.class_fk_id):
            return 400, "Bad Request"

        data = Form.dict()
        questions = data.pop("questions")
        record.update(data, synchronize_session=False)

        # for q_id in questions:
        #     if not db.query(dbm.Questions_form).filter_by(question_pk_id=q_id, deleted=False).first():
        #         return 400, "Bad Request"
        #     record.questions.remove(db.query(dbm.Questions_form).filter_by(question_pk_id=q_id, deleted=False).first())
        #     record.questions.append(db.query(dbm.Questions_form).filter_by(question_pk_id=q_id, deleted=False).first())

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
