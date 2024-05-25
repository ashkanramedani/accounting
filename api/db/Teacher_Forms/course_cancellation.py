from typing import List
from uuid import UUID

from lib import logger

from sqlalchemy.orm import Session
import db.models as dbm
import schemas as sch
from ..Extra import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse, deleted=False).all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course, deleted=False).all()]


def session_cancellation(db: Session, Form: sch.session_cancellation):
    try:
        warnings = []
        sessions_to_cancel = []
        Existing_Subcourse_Session = get_subCourse_active_session(db, Form.sub_course_fk_id)

        for session_id in Form.session_pk_id:
            if session_id not in Existing_Subcourse_Session:
                warnings.append(f'{session_id} is not found.')
                continue
            sessions_to_cancel.append(session_id)

        for session in db.query(dbm.Session_form).filter(dbm.Session_form.session_pk_id.in_(sessions_to_cancel), dbm.Session_form.deleted == False).all():
            session.deleted = True
        db.commit()
        return 200, f"Session cancelled successfully. {' | '.join(warnings)}"

    except Exception as e:
        return Return_Exception(db, e)


def sub_course_cancellation(db: Session, Form: sch.sub_course_cancellation):
    try:
        warnings = []
        message = ''
        Sub_course_to_cancel = []
        Existing_Course_Subcourse = get_Course_active_subcourse(db, Form.course_fk_id)

        for sub_course_id in Form.sub_course_pk_id:
            if sub_course_id not in Existing_Course_Subcourse:
                warnings.append(f'{sub_course_id} is not found.')
                continue
            Sub_course_to_cancel.append(sub_course_id)

        for sub_Course in db.query(dbm.Sub_Course_form).filter(dbm.Sub_Course_form.sub_course_pk_id.in_(Sub_course_to_cancel), dbm.Sub_Course_form.deleted == False).all():
            logger.warning(get_subCourse_active_session(db, sub_Course.sub_course_pk_id))
            status, message = session_cancellation(db, sch.session_cancellation(sub_course_fk_id=sub_Course.sub_course_pk_id, session_pk_id=get_subCourse_active_session(db, sub_Course.sub_course_pk_id)))  # ignore type[call-arg]
            if status != 200:
                return status, message
            sub_Course.deleted = True

        db.commit()
        return 200, f"Sub Course cancelled successfully. {' | '.join(warnings)} ... {message}"

    except Exception as e:
        return Return_Exception(db, e)


def course_cancellation(db: Session, Form: sch.course_cancellation):
    try:

        Course = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_pk_id, deleted=False).first()
        if not Course:
            return 400, "Course Not Found"

        warnings = []
        status, message = sub_course_cancellation(db, sch.sub_course_cancellation(course_fk_id=Form.course_pk_id, sub_course_pk_id=get_Course_active_subcourse(db, Form.course_pk_id)))  # ignore type[call-arg]
        if status != 200:
            return status, message
        Course.deleted = True
        db.commit()
        return 200, f"Course cancelled successfully. {' | '.join(warnings)} ... {message}"

    except Exception as e:
        return Return_Exception(db, e)
