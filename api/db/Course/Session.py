from datetime import datetime, timedelta
from typing import List

from pytz import timezone
from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from ..Extra import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse).filter(dbm.Session_form.status != "deleted").all()]


# ------ Session -------
def get_session(db: Session, session_id):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=session_id).filter(dbm.Session_form.status != "deleted").first()
        if not session:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, session
    except Exception as e:
        return Return_Exception(db, e)


def get_all_session(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Session_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def get_subcourse_session(db: Session, subcourse_id):
    try:
        return 200, db.query(dbm.Session_form).filter_by(sub_course_fk_id=subcourse_id).filter(dbm.Session_form.status != "deleted").all()
    except Exception as e:
        return Return_Exception(db, e)


def get_sub_party(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        QUERY = db.query(dbm.Session_form).filter(dbm.Session_form.status != "deleted", dbm.Session_form.can_accept_sub >= datetime.now(timezone('Asia/Tehran')))
        return record_order_by(db, dbm.Session_form, page, limit, order, SortKey, query=QUERY)
    except Exception as e:
        return Return_Exception(db, e)


def post_session(db: Session, Form: sch.post_session_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        subcourse: dbm.Sub_Course_form = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id).filter(dbm.Sub_Course_form.status != "deleted").first()
        if not subcourse:
            return 400, "Bad Request: sub course not found"

        if not subcourse.sub_course_starting_date <= Form.session_date <= subcourse.sub_course_ending_date:
            return 400, f"Bad Request: session is not in range of subcourse"
        data = Form.__dict__

        current_sessions = db.query(dbm.Session_form).filter_by(sub_course_fk_id=Form.sub_course_fk_id, course_fk_id=subcourse.course_fk_id).filter(dbm.Session_form.status != "deleted").count()
        if subcourse.number_of_session <= current_sessions:
            return 400, "SubCourse is Full"

        can_accept_sub = datetime.combine(Form.session_date, Form.session_starting_time) - timedelta(hours=data.pop("sub_request_threshold"))

        data["days_of_week"] = (Form.session_date.weekday() + 2) % 7
        data["session_ending_time"] = (datetime.combine(datetime.today(), Fix_time(Form.session_starting_time)) + timedelta(minutes=Form.session_duration)).time()
        data["session_teacher_fk_id"] = subcourse.sub_course_teacher_fk_id

        OBJ = dbm.Session_form(**data, session_teacher_fk_id=subcourse.sub_course_teacher_fk_id, can_accept_sub=can_accept_sub)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "session Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_session(db: Session, sub_course: UUID, session: List[UUID], deleted_by: UUID = None):
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
            session.deleted_by = deleted_by
            db.delete(session)
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
        record = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_pk_id).filter(dbm.Session_form.status != "deleted")
        session = record.first()
        if not session:
            return 400, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        subcourse = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=session.sub_course_fk_id).filter(dbm.Sub_Course_form.status != "deleted").first()
        if not subcourse:
            return 400, "Bad Request: parent sub course not found"

        if not subcourse.sub_course_starting_date <= Form.session_date <= subcourse.sub_course_ending_date:
            return 400, f"Bad Request: session is not in range of subcourse"

        data = Form.dict()
        data["can_accept_sub"] = datetime.combine(Form.session_date, Form.session_starting_time) - timedelta(hours=data.pop("sub_request_threshold"))

        record.update(data, synchronize_session=False)
        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_session_status(db: Session, session_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=session_id).first()
        if not record:
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
