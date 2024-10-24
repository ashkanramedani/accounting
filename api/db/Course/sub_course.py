from datetime import timedelta, datetime
from typing import List, Dict

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Course.Session import delete_session
from db.Extra import *
from lib.Date_Time import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse).filter(dbm.Session_form.status != "deleted").all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course).filter(dbm.Sub_Course_form.status != "deleted").all()]


# ------ sub course -------
def get_subcourse(db: Session, subcourse_id):
    try:
        return 200, db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=subcourse_id).filter(dbm.Sub_Course_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_teacher_subcourse(db: Session, teacher_id):
    try:
        return 200, db.query(dbm.Sub_Course_form).filter_by(sub_course_teacher_fk_id=teacher_id).filter(dbm.Sub_Course_form.status != "deleted").all()
    except Exception as e:
        return Return_Exception(db, e)


def get_sub_courses_for_course(db: Session, course_id, page, limit, order, SortKey):
    try:
        sub_course_query = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id).filter(dbm.Sub_Course_form.status != "deleted")
        return record_order_by(db, dbm.Sub_Course_form, page, limit, order, SortKey, query=sub_course_query)

    except Exception as e:
        return Return_Exception(db, e)


def get_all_subcourse(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Sub_Course_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_subcourse(db: Session, Form: sch.post_sub_course_schema):
    try:
        # Validate employee and course existence
        employee_exists = employee_exist(db, [Form.created_fk_by, Form.sub_course_teacher_fk_id])
        if not employee_exists:
            return 400, "Bad Request: employee not found"

        course: dbm.Course_form = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_fk_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "Bad Request: course not found"

        data = Form.__dict__
        session_signature = data.pop("session_signature")
        # Create SubCourse
        sub_course: dbm.Sub_Course_form = create_subcourse(db, data, course)
        sessions: List | None = sub_course.sessions

        # Create Sessions
        if session_signature:
            duplicates = create_sessions(db, Form, sub_course, session_signature, [f'{session.session_date} {session.session_starting_time}' for session in (course.sessions if course.sessions else [])])
            MSG = f"SubCourse Added ( {len(sessions)}/{Form.number_of_session} SESSION ) {duplicates}"
        else:
            MSG = "Empty SubCourse Added ( NO SESSION )"

        db.commit()
        return 200, MSG
    except Exception as e:
        db.rollback()
        return Return_Exception(db, e)


def create_subcourse(db: Session, sub_course_data: Dict, course) -> dbm.Sub_Course_form:
    course_data = {"sub_course_capacity": course.course_capacity, "sub_course_available_seat": course.course_capacity}
    sub_course = dbm.Sub_Course_form(**sub_course_data, **course_data)  # type: ignore
    db.add(sub_course)
    db.flush()
    return sub_course


def create_sessions(db: Session, Form: sch.post_sub_course_schema, sub_course: dbm.Sub_Course_form, session_signature: dict, existing_sessions: List[str]):
    Session_signature = {}
    sub_request_threshold = Form.sub_request_threshold

    for i in session_signature:
        if i.days_of_week not in Session_signature:
            Session_signature[i.days_of_week] = []
        Session_signature[i.days_of_week].append((i.starting_time, i.duration))

    date_table = generate_time_table(
            starting_date=Form.sub_course_starting_date,
            ending_date=Fix_date(Form.sub_course_ending_date),
            day_of_week=Session_signature.keys())

    WARN = []
    for day_date, day_weekday in date_table[:Form.number_of_session]:
        for start_time, session_duration in Session_signature[day_weekday]:
            session_starting_time = datetime.combine(day_date, Fix_time(start_time))

            SIG = f'{session_starting_time}'
            if SIG in existing_sessions:
                WARN.append(f"{SIG} - Already Exist")
                continue

            session_ending_time = session_starting_time + timedelta(minutes=session_duration)
            can_accept_sub = datetime.combine(day_date, session_starting_time.time()) - timedelta(hours=sub_request_threshold)

            session_data = {
                "created_fk_by": Form.created_fk_by,
                "course_fk_id": Form.course_fk_id,
                "sub_course_fk_id": sub_course.sub_course_pk_id,
                "session_teacher_fk_id": Form.sub_course_teacher_fk_id,
                "session_date": day_date,
                "session_starting_time": session_starting_time.time(),
                "session_ending_time": session_ending_time.time(),
                "session_duration": session_duration,
                "days_of_week": day_weekday,
                "can_accept_sub": can_accept_sub}
            db.add(dbm.Session_form(**session_data))  # type: ignore[call-arg]
    db.flush()
    return WARN


def delete_subcourse(db: Session, course_id: UUID, sub_course_ids: List[UUID], deleted_by: UUID = None):
    try:
        warnings = []
        message = ''
        Sub_course_to_cancel = []
        if not sub_course_ids:
            return 400, "No SubCourse Provided"
        if not course_id:
            course_id = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=sub_course_ids[0]).first().course_fk_id

        Existing_Course_Subcourse = get_Course_active_subcourse(db, course_id)

        for sub_course_id in sub_course_ids:
            if sub_course_id not in Existing_Course_Subcourse:
                warnings.append(f'{sub_course_id} is not found.')
                continue
            Sub_course_to_cancel.append(sub_course_id)

        for sub_Course in db.query(dbm.Sub_Course_form).filter(dbm.Sub_Course_form.sub_course_pk_id.in_(Sub_course_to_cancel), dbm.Sub_Course_form.deleted == False).all():
            status, message = delete_session(db, sub_Course.sub_course_pk_id, get_subCourse_active_session(db, sub_Course.sub_course_pk_id))  # ignore type[call-arg]
            if status != 200:
                return status, message

            sub_Course._Deleted_By = deleted_by
            db.delete(sub_Course)
        db.commit()
        return 200, f"Sub Course cancelled successfully. {' | '.join(warnings)} ... {message}"

    except Exception as e:
        return Return_Exception(db, e)


def update_subcourse(db: Session, Form: sch.update_sub_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"
        record = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_pk_id).filter(dbm.Sub_Course_form.status != "deleted")
        if not record.first():
            return 400, "Record Not Found"

        data = Form.__dict__
        if "session_signature" in data:
            data.pop("session_signature")
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_subcourse_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=form_id).first()
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
