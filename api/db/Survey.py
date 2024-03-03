import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


# question
def get_question(db: Session, question_id):
    try:
        return 200, db.query(dbm.Questions_form).filter_by(question_pk_id=question_id, deleted=False).first()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_question(db: Session):
    try:
        return 200, db.query(dbm.Questions_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_question(db: Session, Form: sch.post_questions_schema):
    try:
        OBJ = dbm.Questions_form()
        OBJ.text = Form.text

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
        record = db.query(dbm.Remote_Request_form).filter_by(question_id_pk_id=question_id,deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_question(db: Session, Form: sch.update_questions_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(question_pk_id=Form.question_pk_id,deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        data["update_date"] = datetime.now(timezone.utc).astimezone()
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# survey
def get_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.survey_form).filter_by(survey_pk_id=survey_id,deleted=False).first()
        if record:
            res = {k: v for k, v in record.__dict__.items()}
            res["questions"] = [db.query(dbm.survey_questions_form).filter_by(survey_fk_id=record.survey_pk_id).all]
            return 200, res
        return 200, []
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_survey(db: Session):
    try:
        result = []
        data = db.query(dbm.survey_form).filter_by(deleted=False).all()
        if data:
            for record in data:
                res = {k: v for k, v in record.__dict__.items()}
                print(f'{db.query(dbm.survey_questions_form).filter_by(survey_fk_id=record.survey_pk_id).all = }')
                res["questions"] = [db.query(dbm.survey_questions_form).filter_by(survey_fk_id=record.survey_pk_id).all]
                result.append(res)
            return 200, result
        return 200, []
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_survey(db: Session, Form: sch.post_survey_schema):
    try:
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 400, "Bad Request"

        OBJ = dbm.survey_form()
        OBJ.title = Form.title
        OBJ.class_fk_id = Form.class_fk_id

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        form_uuid = OBJ.survey_pk_id

        for uuid in Form.questions:
            Q_OBJ = dbm.survey_questions_form()
            Q_OBJ.question_fk_id = uuid
            Q_OBJ.survey_fk_id = form_uuid
            db.add(Q_OBJ)
            db.commit()
            db.refresh(Q_OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(survey_id_pk_id=survey_id,deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True

        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_survey(db: Session, Form: sch.update_survey_schema):
    try:
        record = db.query(dbm.survey_form).filter_by(survey_pk_id=Form.survey_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 400, "Bad Request"

        record.class_fk_id = Form.class_fk_id
        record.title = Form.title
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
