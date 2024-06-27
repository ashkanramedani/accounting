from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from db import models as dbm
import schemas as sch
from lib import logger
from ..Extra import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse, deleted=False
                                                                                      ).all()]


# ------ Session -------
def get_session(db: Session, session_id):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=session_id, deleted=False).first()
        if not session:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, session
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_session(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Session_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_sub_party(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        now = datetime.now()
        return 200, record_order_by(db, dbm.Session_form, page, limit, order, query=db.query(dbm.Session_form).filter(dbm.Session_form.can_accept_sub >= now))
    except Exception as e:
        return Return_Exception(db, e)


def post_session(db: Session, Form: sch.post_session_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.session_teacher_fk_id]):
            return 400, "Bad Request: employee not found"

        subcourse = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id, deleted=False).first()
        if not subcourse:
            return 400, "Bad Request: sub course not found"

        data = Form.__dict__

        current_sessions = db.query(dbm.Session_form).filter_by(sub_course_fk_id=data["sub_course_fk_id"], course_fk_id=data["course_fk_id"], deleted=False).count()
        if subcourse.number_of_session >= current_sessions:
            return 400, "SubCourse is Full"

        can_accept_sub = datetime.combine(data["session_date"], data["session_starting_time"]) - timedelta(hours=data.pop("sub_request_threshold"))
        OBJ = dbm.Session_form(**data, can_accept_sub=can_accept_sub)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "session Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_session(db: Session, sub_course: UUID, session: List[UUID]):
    try:
        warnings = []
        sessions_to_cancel = []
        Existing_Subcourse_Session = get_subCourse_active_session(db, sub_course)

        for session_id in session:
            if session_id not in Existing_Subcourse_Session:
                warnings.append(f'{session_id} is not found.')
                continue
            sessions_to_cancel.append(session_id)

        for session in db.query(dbm.Session_form).filter(dbm.Session_form.session_pk_id.in_(sessions_to_cancel), dbm.Session_form.deleted == False).all():
            session.deleted = True
        db.commit()
        return 200, f"Session deleted successfully. {' | '.join(warnings)}"
    except Exception as e:
        return Return_Exception(db, e)


def cancel_session(db: Session, sub_course: UUID, session: List[UUID]):
    try:
        warnings = []
        sessions_to_cancel = []
        Existing_Subcourse_Session = get_subCourse_active_session(db, sub_course)

        for session_id in session:
            if session_id not in Existing_Subcourse_Session:
                warnings.append(f'{session_id} is not found.')
                continue
            sessions_to_cancel.append(session_id)

        for session in db.query(dbm.Session_form).filter(dbm.Session_form.session_pk_id.in_(sessions_to_cancel), dbm.Session_form.deleted == False, dbm.Session_form.canceled == False).all():
            session.canceled = True
        db.commit()
        return 200, f"Session cancelled successfully. {' | '.join(warnings)}"
    except Exception as e:
        return Return_Exception(db, e)


def update_session(db: Session, Form: sch.update_session_schema):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_pk_id, deleted=False)
        if not record.first():
            return 400, "Record Not Found"

        data = Form.dict()
        data["can_accept_sub"] = datetime.combine(data["session_date"], data["session_starting_time"]) - timedelta(hours=data.pop("sub_request_threshold"))
        OBJ = dbm.Session_form(**data, can_accept_sub=can_accept_sub)  # type: ignore[call-arg]

        record.update(data, synchronize_session=False)
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
