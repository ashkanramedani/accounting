from typing import List, Dict
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .sub_course import delete_subcourse
from ..Extra import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse).filter(dbm.Session_form.status != "deleted").all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course).filter(dbm.Sub_Course_form.status != "deleted").all()]


def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "Bad Request: Course Not Found"
        sub_course = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id).filter(dbm.Sub_Course_form.status != "deleted").all()
        if not sub_course:
            course.teachers = []
            course.session_signature = []
            course.available_seat = course.course_capacity
            return 200, course

        Unique_signature: List = db \
            .query(dbm.Session_form.days_of_week) \
            .filter_by(course_fk_id=course_id) \
            .filter(dbm.Session_form.status != "deleted") \
            .distinct(dbm.Session_form.days_of_week) \
            .all()

        course.teachers = [sub_course.teacher for sub_course in sub_course]
        course.session_signature = [day["days_of_week"] for day in Unique_signature]
        course.available_seat = min([SB.sub_course_available_seat for SB in sub_course])
        course.number_of_session = 0

        return 200, course
    except Exception as e:
        return Return_Exception(db, e)


def get_all_course(db: Session, course_type: str | None, page: sch.NonNegativeInt, limit: sch.PositiveInt, SortKey: str, order: str = "desc"):
    try:
        if course_type:
            Course_type = db.query(dbm.Course_Type_form).filter_by(course_type_name=course_type).first().course_type_pk_id
            if Course_type:
                status, courses = record_order_by(db, dbm.Course_form, page, limit, order, SortKey, course_type=Course_type)
            else:
                status, courses = 200, []
        else:
            status, courses = record_order_by(db, dbm.Course_form, page, limit, order, SortKey)
        if status != 200:
            return status, courses

        Courses = []
        for course in courses:
            sub_course: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course.course_pk_id).filter(dbm.Sub_Course_form.status != "deleted").all()

            if not sub_course:
                course.teachers = []
                course.session_signature = []
                course.available_seat = course.course_capacity
                Courses.append(course)
                continue

            course.teachers = [OBJ.teacher for OBJ in sub_course]

            Unique_signature: List = db \
                .query(dbm.Session_form.days_of_week) \
                .filter_by(course_fk_id=course.course_pk_id) \
                .filter(dbm.Session_form.status != "deleted") \
                .distinct(dbm.Session_form.days_of_week) \
                .all()

            course.session_signature = [day["days_of_week"] for day in Unique_signature]
            course.available_seat = min([OBJ.sub_course_available_seat for OBJ in sub_course])
            course.number_of_session = 0  # NC: count the number of of session
            Courses.append(course)

        return 200, Courses
    except Exception as e:
        return Return_Exception(db, e)


def post_course(db: Session, Form: sch.post_course_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"

        data = Form.__dict__

        tags = data.pop("tags") if "tags" in data else []
        categories = data.pop("categories") if "categories" in data else []

        OBJ = dbm.Course_form(**data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        Warn = Add_tags_category(db, OBJ, OBJ.course_pk_id, tags, categories)

        return 201, sch.Base_record_add(Warning=' | '.join(Warn), id=OBJ.course_pk_id)
    except Exception as e:
        return Return_Exception(db, e)


def delete_course(db: Session, course_id):
    try:

        Course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not Course:
            return 400, "Course Not Found"

        warnings = []
        status, message = delete_subcourse(db, course_id, get_Course_active_subcourse(db, course_id))  # ignore type[call-arg]
        if status != 200:
            return status, message
        Course.deleted = True
        db.commit()
        return 200, f"Course cancelled successfully. {' | '.join(warnings)} ... {message}"

    except Exception as e:
        return Return_Exception(db, e)


def update_course(db: Session, Form: sch.update_course_schema):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_pk_id).filter(dbm.Course_form.status != "deleted")
        if not course.first():
            return 404, "Course Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: employee not found"
        data = Form.__dict__

        tags: List[sch.Update_Relation] = data.pop("tags")
        categories: List[sch.Update_Relation] = data.pop("categories")

        course.update(data, synchronize_session=False)
        db.commit()
        Errors = Add_tags_category(db, course.first(), Form.course_pk_id, tags, categories)
        if Errors:
            return 200, "Course updated but there was an error in the tags or categories: " + ", ".join(Errors)
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
