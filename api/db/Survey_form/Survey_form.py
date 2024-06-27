from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from db import models as dbm
import schemas as sch
from ..Extra import *


def get_all_survey(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Survey_form, page, limit, order)

    except Exception as e:
        return Return_Exception(db, e)


def post_survey(db: Session, Form: sch.post_survey_schema):
    try:
        if not db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id, deleted=False).first():
            return 400, "Bad Request: Sub Course not found"

        data = Form.dict()
        questions: List[UUID] = data.pop("questions") if "questions" in data else []

        OBJ = dbm.Survey_form(**data)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if not questions:
            return 200, "Empty survey added"

        question_ID: List[UUID] = [ID.question_pk_id for ID in db.query(dbm.Question_form).filter_by(deleted=False).all()]

        for q_id in questions:
            if q_id not in question_ID:
                return 400, "Bad Request"
            OBJ.questions.append(db.query(dbm.Question_form).filter_by(question_pk_id=q_id, deleted=False).first())
        db.commit()
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_survey(db: Session, survey_id):
    try:
        record = db.query(dbm.Survey_form).filter_by(survey_id_pk_id=survey_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True

        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_survey(db: Session, Form: sch.update_survey_schema):
    try:
        record = db.query(dbm.Survey_form).filter_by(survey_pk_id=Form.survey_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not course_exist(db, Form.sub_course_fk_id):
            return 400, "Bad Request: Sub Course not found"

        data = Form.dict()
        if "questions" not in data:
            return 200, "Form Updated"

        record.update(data, synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)
