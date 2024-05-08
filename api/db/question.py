from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger

from .Extra import record_order_by

# question
def get_question(db: Session, question_id):
    try:
        return 200, db.query(dbm.Question_form).filter_by(question_pk_id=question_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_question(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Question_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_question(db: Session, Form: sch.post_questions_schema):
    try:
        OBJ = dbm.Question_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_question(db: Session, question_id):
    try:
        record = db.query(dbm.Question_form).filter_by(question_pk_id=question_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_question(db: Session, Form: sch.update_questions_schema):
    try:
        record = db.query(dbm.Question_form).filter_by(question_pk_id=Form.question_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


# survey
def get_survey(db: Session, survey_id):
    try:
        return 200, db.query(dbm.Survey_form).filter_by(survey_pk_id=survey_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
