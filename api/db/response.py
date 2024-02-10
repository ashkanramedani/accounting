from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


# response
def get_response(db: Session, response_id):
    try:
        record = db.query(dbm.response_form).filter_by(
                response_pk_id=response_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def get_all_response(db: Session):
    try:
        data = db.query(dbm.response_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_response(db: Session, Form: sch.post_response_schema):
    try:
        if not db.query(dbm.Student_form).filter_by(student_pk_id=Form.student_fk_id, deleted=False).first():
            return 404, "Target student Not found"

        if not db.query(dbm.Questions_form).filter_by(question_pk_id=Form.question_fk_id, deleted=False).first():
            return 404, "Target Question Not found"

        if not db.query(dbm.survey_form).filter_by(form_pk_id=Form.form_fk_id, deleted=False).first():
            return 404, "Target Survey Not found"

        OBJ = dbm.response_form()

        OBJ.student_fk_id = Form.student_fk_id
        OBJ.question_fk_id = Form.question_fk_id
        OBJ.form_fk_id = Form.form_fk_id
        OBJ.answer = Form.answer

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "response Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def delete_response(db: Session, response_id):
    try:
        record = db.query(dbm.response_form).filter_by(
                response_pk_id=response_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_response(db: Session, Form: sch.update_response_schema):
    try:
        record = db.query(dbm.response_form).filter_by(
                response_pk_id=Form.response_pk_id,
                delete=False
        ).first()

        if not record:
            return 404, "Not Found"

        if not db.query(dbm.Student_form).filter_by(student_pk_id=Form.student_fk_id, deleted=False).first():
            return 404, "Target student Not found"

        if not db.query(dbm.Questions_form).filter_by(question_pk_id=Form.question_fk_id, deleted=False).first():
            return 404, "Target Question Not found"

        if not db.query(dbm.survey_form).filter_by(form_pk_id=Form.form_fk_id, deleted=False).first():
            return 404, "Target Survey Not found"

        record.student_fk_id = Form.student_fk_id
        record.question_fk_id = Form.question_fk_id
        record.form_fk_id = Form.form_fk_id
        record.answer = Form.answer
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()

#
