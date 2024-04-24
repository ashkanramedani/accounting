from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger

from ..Extra import *
from lib.Date_Time import *
from datetime import timedelta, datetime


def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: Course Not Found"
        sub_course = db.query(dbm.sub_course_form).filter_by(course_fk_id=course_id, deleted=False).all()
        if not sub_course:
            course.sub_course = []
            return 200, course.__dict__ | {"teachers": [], "session_signature": [], "available_seat": course.course_capacity}
        extra = {
            "teachers": [sub_course.teacher for sub_course in sub_course],
            # "session_signature": [sub_course.session_signature for sub_course in sub_course],
            "session_signature": [],
            "available_seat": min([sub_course.sub_course_available_seat for sub_course in sub_course]),
        }

        return 200, course.__dict__ | extra
    except Exception as e:
        logger.error(e)
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
                Courses.append(course.__dict__ | {"teachers": [], "session_signature": [], "available_seat": course.course_capacity})
                continue
            extra = {
                "teachers": [sub_course.teacher for sub_course in sub_course],
                # "session_signature": [sub_course.session_signature for sub_course in sub_course],
                "session_signature": [],
                "available_seat": min([sub_course.sub_course_available_seat for sub_course in sub_course]),
            }
            Courses.append(course.__dict__ | extra)
        return 200, Courses
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_course(db: Session, Form: sch.post_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        data = Form.__dict__
        tags_id = [tag.tag_pk_id for tag in db.query(dbm.Tag_form).filter_by(deleted=False).all()]
        categories_id = [category.category_pk_id for category in db.query(dbm.Category_form).filter_by(deleted=False).all()]

        tags = data.pop("tags")
        categories = data.pop("categories")

        OBJ = dbm.course_form(**data)  # type: ignore[call-arg]

        for tag in tags:
            if tag not in tags_id:
                return 400, "Bad Request: tag not found"
            OBJ.tags.append(db.query(dbm.Tag_form).filter_by(tag_pk_id=tag, deleted=False).first())
        for category in categories:
            if category not in categories_id:
                return 400, "Bad Request: category not found"
            OBJ.categories.append(db.query(dbm.Category_form).filter_by(category_pk_id=category, deleted=False).first())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, "course Added"
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_course(db: Session, Form: sch.update_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"
        data = Form.__dict__
        if "session_signature" in data:
            data.pop("session_signature")
        record = db.query(dbm.course_form).filter_by(course_pk_id=Form.course_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
