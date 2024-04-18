from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from .Extra import *
from lib.Date_Time import *
from datetime import timedelta, datetime

def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: Course Not Found"
        sub_course = db.query(dbm.sub_course_form).filter_by(course_fk_id=course_id, deleted=False).all()
        if not sub_course:
            return 200, course
        extra = {
            "teachers": [sub_course.teacher for sub_course in sub_course],
            "course_number_of_session": sum([sub_course.number_of_session for sub_course in sub_course]),
            "session_signature": [sub_course.course_signature for sub_course in sub_course],
            "available_seat": sum([sub_course.available_seat for sub_course in sub_course]),
            "total_seat": sum([sub_course.total_seat for sub_course in sub_course])
        }

        """
            teachers: List[UUID]
            course_number_of_session: int = 0
            session_signature: List[Session_signature] = []
            available_seat: int
            total_seat: int
        """
        return 200, course.__dict__ | extra
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_course(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        courses = record_order_by(db, dbm.course_form, page, limit, order)
        if not courses:
            return 200, []
        Courses = []
        for course in courses:
            sub_course = db.query(dbm.sub_course_form).filter_by(course_fk_id=course.course_pk_id, deleted=False).all()
            if not sub_course:
                course.sub_course = []
                continue
            extra = {
                "teachers": [sub_course.teacher for sub_course in sub_course],
                "course_number_of_session": sum([sub_course.number_of_session for sub_course in sub_course]),
                "session_signature": [sub_course.course_signature for sub_course in sub_course],
                "available_seat": min([sub_course.available_seat for sub_course in sub_course]),
                "total_seat": sum([sub_course.total_seat for sub_course in sub_course])
            }
            Courses.append(course.__dict__ | extra)
        return 200, Courses
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_course(db: Session, Form: sch.post_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        data = Form.__dict__
        tags_id = [tag.tag_pk_id for tag in db.query(dbm.Tag_form).filter_by(deleted=False).all()]
        categories_id = [category.category_pk_id for category in db.query(dbm.Categories).filter_by(deleted=False).all()]

        tags = data.pop("tags")
        categories = data.pop("categories")


        OBJ = dbm.course_form(**data)  # type: ignore[call-arg]

        for tag in tags:
            if tag not in tags_id:
                return 400, "Bad Request: tag not found"
            OBJ.tags.append(db.query(dbm.Tag_form).filter_by(tag_pk_id=tag, deleted=False).first())
        for category in categories:
            if category not in categories:
                return 400, "Bad Request: category not found"
            OBJ.categories.append(db.query(dbm.Category_form).filter_by(category_pk_id=category, deleted=False).first())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "course Added"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_course(db: Session, course_id):
    try:
        record = db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_course(db: Session, Form: sch.update_course_schema):
    try:
        record = db.query(dbm.course_form).filter_by(course_pk_id=Form.course_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

# ------ sub course -------
def get_subcourse(db: Session, subcourse_id):
    try:
        sub_course = db.query(dbm.sub_course_form).filter_by(sub_course_pk_id=subcourse_id, deleted=False).first()
        if not sub_course:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, sub_course
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_subcourse(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return record_order_by(db, dbm.course_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_subcourse(db: Session, Form: sch.post_sub_course_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        if not db.query(dbm.Employees_form).filter_by(employee_pk_id=Form.sub_course_teacher_fk_id, deleted=False).first():
            return 400, "Bad Request: teacher not found"

        course = db.query(dbm.course_form).filter_by(course_pk_id=Form.course_fk_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: course not found"


        data = Form.__dict__
        session_signature = {day: (start, duration) for day, start, duration in data.pop("session_signature")}
        OBJ = dbm.sub_course_form(**data, course_capacity=course.course_capacity) # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)


        if not session_signature:
            return 200, "Empty SubCourse Added ( NO SESSION )"

        date_table = generate_time_table(
                starting_date=Form.sub_course_starting_date,
                ending_date=Fix_date(Form.sub_course_ending_date),
                day_of_week=session_signature.keys())
        days = []
        for day_date, day_weekday in date_table:
            start_time, session_duration = session_signature[day_weekday]
            session_starting_time = datetime.combine(day_date, Fix_time(start_time))
            session_ending_time = session_starting_time + timedelta(minutes=session_duration)


            session_data = {
                "course_fk_id": Form.course_fk_id,
                "sub_course_fk_id": OBJ.sub_course_pk_id,
                "session_main_teacher_fk_id": Form.sub_course_teacher_fk_id,
                "session_sub_teacher_fk_id": None,
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
        logger.error(f'{e.__class__.__name__}: {e.args}')
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
        logger.error(f'{e.__class__.__name__}: {e.args}')
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
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

# ------ Session -------
def get_session(db: Session, session_id):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=session_id, deleted=False).first()
        if not session:
            return 400, "Bad Request: Sub Course Not Found"

        return 200, session
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_session(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return record_order_by(db, dbm.Session_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_session(db: Session, Form: sch.post_session_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.session_teacher_fk_id]):
            return 400, "Bad Request: employee not found"

        if not db.query(dbm.sub_course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id, deleted=False).first():
            return 400, "Bad Request: sub course not found"

        if not db.query(dbm.course_form).filter_by(course_pk_id=Form.course_fk_id, deleted=False).first():
            return 400, "Bad Request: course not found"

        OBJ = dbm.Session_form(**Form.__dict__) # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "session Added"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_session(db: Session, course_id):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=course_id, deleted=False).first()
        if not record:
            return 400, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_session(db: Session, Form: sch.update_session_schema):
    try:
        record = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_pk_id, deleted=False)
        if not record.first():
            return 400, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
