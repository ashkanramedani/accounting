from lib import log

logger = log()
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# response
def get_response(db: Session, response_id):
    try:
        return 200, db.query(dbm.Response_form).filter_by(response_pk_id=response_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_response(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Response_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_response(db: Session, Form: sch.post_response_schema):
    try:
        if not db.query(dbm.Student_form).filter_by(student_pk_id=Form.student_fk_id, deleted=False).first():
            return 400, "Bad Request"

        if not db.query(dbm.Questions_form).filter_by(question_pk_id=Form.question_fk_id, deleted=False).first():
            return 400, "Bad Request"

        if not db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_fk_id, deleted=False).first():
            return 400, "Bad Request"

        OBJ = dbm.Response_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "response Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_response(db: Session, response_id):
    try:
        record = db.query(dbm.Response_form).filter_by(response_pk_id=response_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_response(db: Session, Form: sch.update_response_schema):
    try:
        record = db.query(dbm.Response_form).filter_by(response_pk_id=Form.response_pk_id, deleted=False)

        if not record.first():
            return 404, "Record Not Found"

        if not db.query(dbm.Student_form).filter_by(student_pk_id=Form.student_fk_id, deleted=False).first():
            return 400, "Bad Request"

        if not db.query(dbm.Questions_form).filter_by(question_pk_id=Form.question_fk_id, deleted=False).first():
            return 400, "Bad Request"

        if not db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_fk_id, deleted=False).first():
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
