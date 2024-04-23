import json

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger, JSONEncoder

from ..Extra import *
from lib.Date_Time import *
from datetime import timedelta, datetime


# ------ sub course -------
def get_subcourse(db: Session, subcourse_id):
    try:
        sub_course = db.query(dbm.sub_course_form).filter_by(sub_course_pk_id=subcourse_id, deleted=False).first()
        if not sub_course:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, sub_course
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_subcourse(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.sub_course_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_subcourse(db: Session, Form: sch.post_sub_course_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=Form.sub_course_teacher_fk_id, deleted=False).first():
            return 400, "Bad Request: teacher not found"

        course = db.query(dbm.course_form).filter_by(course_pk_id=Form.course_fk_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: course not found"


        data = Form.__dict__

        session_signature = data.pop("session_signature")

        data |= {"sub_course_capacity": course.course_capacity, "sub_course_available_seat": course.course_capacity}
        OBJ = dbm.sub_course_form(**data)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if not session_signature:
            return 200, "Empty SubCourse Added ( NO SESSION )"

        date_table = generate_time_table(
                starting_date=Form.sub_course_starting_date,
                ending_date=Fix_date(Form.sub_course_ending_date),
                day_of_week=[record.days_of_week for record in session_signature])

        days = []

        for day_date, day_weekday in date_table:
            start_time, session_duration = None, None
            for day in session_signature:
                if day_weekday == day.days_of_week:
                    start_time, session_duration = day.starting_time, day.duration
                    break
            if not start_time:
                continue
            session_starting_time = datetime.combine(day_date, Fix_time(start_time))
            session_ending_time = session_starting_time + timedelta(minutes=session_duration)

            session_data = {
                "created_fk_by": Form.created_fk_by,
                "course_fk_id": Form.course_fk_id,
                "sub_course_fk_id": OBJ.sub_course_pk_id,
                "session_teacher_fk_id": Form.sub_course_teacher_fk_id,
                "session_date": day_date,
                "session_starting_time": session_starting_time,
                "session_ending_time": session_ending_time,
                "session_duration": session_duration,
                "days_of_week": day_weekday,
            }
            days.append(dbm.Session_form(**session_data))  # type: ignore[call-arg]

        db.add_all(days)
        db.commit()
        return 200, "SubCourse Added ( WITH SESSION )"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_subcourse(db: Session, course_id):
    try:
        record = db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not record:
            return 400, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_subcourse(db: Session, Form: sch.update_sub_course_schema):
    try:
        record = db.query(dbm.sub_course_form).filter_by(sub_course_pk_id=Form.sub_course_pk_id, deleted=False)
        if not record.first():
            return 400, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
