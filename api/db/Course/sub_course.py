import json
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger, JSONEncoder

from ..Extra import *
from lib.Date_Time import *
from datetime import timedelta, datetime

from .Session import delete_session


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse, deleted=False).all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course, deleted=False).all()]


# ------ sub course -------
def get_subcourse(db: Session, subcourse_id):
    try:
        sub_course = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=subcourse_id, deleted=False).first()
        if not sub_course:
            return 200, []

        return 200, sub_course
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_subcourse(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Sub_Course_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_subcourse(db: Session, Form: sch.post_sub_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.sub_course_teacher_fk_id]):
            return 400, "Bad Request: employee not found"

        course = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_fk_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: course not found"

        data = Form.__dict__

        session_signature = data.pop("session_signature")
        data |= {"sub_course_capacity": course.course_capacity, "sub_course_available_seat": course.course_capacity}
        OBJ = dbm.Sub_Course_form(**data)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
    except Exception as e:
        return Return_Exception(db, e)

    try:
        if not session_signature:
            return 200, "Empty SubCourse Added ( NO SESSION )"

        Session_signature = {}
        for i in session_signature:
            if i.days_of_week not in Session_signature:
                Session_signature[i.days_of_week] = []
            Session_signature[i.days_of_week].append((i.starting_time, i.duration))

        date_table = generate_time_table(
                starting_date=Form.sub_course_starting_date,
                ending_date=Fix_date(Form.sub_course_ending_date),
                day_of_week=Session_signature.keys())

        days = []
        for day_date, day_weekday in date_table[:data["number_of_session"]]:
            for start_time, session_duration in Session_signature[day_weekday]:
                session_starting_time = datetime.combine(day_date, Fix_time(start_time))
                session_ending_time = session_starting_time + timedelta(minutes=session_duration)

                session_data = {
                    "created_fk_by": Form.created_fk_by,
                    "course_fk_id": Form.course_fk_id,
                    "sub_course_fk_id": OBJ.sub_course_pk_id,
                    "session_teacher_fk_id": Form.sub_course_teacher_fk_id,
                    "session_date": day_date,
                    "session_starting_time": session_starting_time.time(),
                    "session_ending_time": session_ending_time.time(),
                    "session_duration": session_duration,
                    "days_of_week": day_weekday}

                days.append(dbm.Session_form(**session_data))  # type: ignore[call-arg]
        db.add_all(days)
        db.commit()
        return 200, "SubCourse Added ( WITH SESSION )"
    except Exception as e:
        db.rollback()
        try:
            OBJ.deleted = True
            OBJ.description = "Deleted due to an error in session creation"
            db.commit()
        except Exception as inner_e:
            db.rollback()
            return Return_Exception(db, inner_e)
        return Return_Exception(db, e)


def delete_subcourse(db: Session, course_id, sub_course_id: sch.delete_sub_course_schema):
    try:
        warnings = []
        message = ''
        Sub_course_to_cancel = []
        Existing_Course_Subcourse = get_Course_active_subcourse(db, course_id)

        for sub_course_id in sub_course_id:
            if sub_course_id not in Existing_Course_Subcourse:
                warnings.append(f'{sub_course_id} is not found.')
                continue
            Sub_course_to_cancel.append(sub_course_id)

        for sub_Course in db.query(dbm.Sub_Course_form).filter(dbm.Sub_Course_form.sub_course_pk_id.in_(Sub_course_to_cancel), dbm.Sub_Course_form.deleted == False).all():
            logger.warning(get_subCourse_active_session(db, sub_Course.sub_course_pk_id))
            status, message = delete_session(db, sub_course_id, get_subCourse_active_session(db, sub_Course.sub_course_pk_id))  # ignore type[call-arg]
            if status != 200:
                return status, message
            sub_Course.deleted = True

        db.commit()
        return 200, f"Sub Course cancelled successfully. {' | '.join(warnings)} ... {message}"

    except Exception as e:
        return Return_Exception(db, e)


def update_subcourse(db: Session, Form: sch.update_sub_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"
        record = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_pk_id, deleted=False)
        if not record.first():
            return 400, "Record Not Found"

        data = Form.__dict__
        if "session_signature" in data:
            data.pop("session_signature")
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
