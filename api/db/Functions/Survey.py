import logging
from uuid import UUID

from sqlalchemy.orm import Session
from typing import List
import schemas as sch
import db.models as dbm
from .Exist import employee_exist


# question
def get_question(db: Session, question_id):
    try:
        record = db.query(dbm.Questions_form).filter_by(
                question_pk_id=question_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_question(db: Session):
    try:
        data = db.query(dbm.Questions_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_question(db: Session, Form: sch.post_questions_schema):
    try:
        OBJ = dbm.Questions_form(text=Form.text)
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_question(db: Session, question_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                question_id_pk_id=question_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_question_id(db: Session, Form: sch.update_questions_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                question_pk_id=Form.question_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        record.text = Form.text

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()

# survey
def get_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.survey_form).filter_by(
                survey_pk_id=survey_id,
                deleted=False
        ).first()
        if record:
            record["questions"] = [db.query(dbm.survey_questions_form).filter_by(form_fk_id=record.form_pk_id).all]
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_survey(db: Session):
    try:
        data = db.query(dbm.survey_form).filter_by(deleted=False).all()
        if data:
            for record in data:
                record["questions"] = [db.query(dbm.survey_questions_form).filter_by(form_fk_id=record.form_pk_id).all]
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_survey(db: Session, Form: sch.post_survey_schema):
    try:
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        OBJ = dbm.Questions_form(title=Form.title)
        db.add(OBJ)

        form_uuid = OBJ.form_pk_id
        for uuid in Form.questions:
            Q_OBJ = dbm.survey_questions_form(form_fk_id=form_uuid, question_fk_id=uuid)
            db.add(Q_OBJ)

        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                survey_id_pk_id=survey_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True

        for survey_questions in db.query(dbm.survey_questions_form).filter_by(form_fk_id=record.form_pk_id).all:
            survey_questions.deleted = False

        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_survey(db: Session, Form: sch.update_survey_schema):
    try:
        record = db.query(dbm.survey_form).filter_by(
                form_pk_id=Form.form_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        record.class_fk_id = Form.class_fk_id
        record.title = Form.title

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()

def update_survey_question(db: Session, Form: sch.update_survey_question_schema):
    try:
        record = db.query(dbm.survey_questions_form).filter_by(
                form_pk_id=Form.form_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        record.questions_fk_id = Form.questions_fk_id
        record.title = Form.new_question_fk_id

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
