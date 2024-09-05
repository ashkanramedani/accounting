from sqlalchemy.orm import Session

import schemas as sch
import models as dbm
from ..Extra import *


# question
def get_question(db: Session, question_id):
    try:
        return 200, db.query(dbm.Question_form).filter_by(question_pk_id=question_id).filter(dbm.Question_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_question(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Question_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_question(db: Session, Form: sch.post_questions_schema):
    try:
        if not db.query(dbm.Language_form).filter(dbm.Language_form.status != "deleted").count():
            return 400, "Bad Request: No language found"
        OBJ = dbm.Question_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_question(db: Session, question_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Question_form).filter_by(question_pk_id=question_id).filter(dbm.Question_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_question(db: Session, Form: sch.update_questions_schema):
    try:
        record = db.query(dbm.Question_form).filter_by(question_pk_id=Form.question_pk_id).filter(dbm.Question_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


# survey
def get_survey(db: Session, survey_id):
    try:
        return 200, db.query(dbm.Survey_form).filter_by(survey_pk_id=survey_id).filter(dbm.Survey_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)
