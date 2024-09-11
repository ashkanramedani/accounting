from typing import List

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from lib import logger
from .sub_course import delete_subcourse
from ..Extra import *


def available_seat_for_subcourse(db: Session, subcourse: dbm.Sub_Course_form):
    seat_in_queue: int = db.query(dbm.SignUp_queue).filter_by(subcourse_fk_id=subcourse.sub_course_pk_id).count()
    reserved_seat: int = db.query(dbm.SignUp_form).filter_by(subcourse_fk_id=subcourse.sub_course_pk_id).count()
    return subcourse.sub_course_capacity - seat_in_queue - reserved_seat

def course_additional_details(db: Session, course: dbm.Course_form):

    sub_course: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course.course_pk_id).filter(dbm.Sub_Course_form.status != "deleted").all()

    if not sub_course:
        course.teachers = []
        course.session_signature = []
        course.available_seat = course.course_capacity
        course.available_seat_for_subcourse = {}
        course.number_of_session = {}

    Unique_signature: List = db \
        .query(dbm.Session_form.days_of_week) \
        .filter_by(course_fk_id=course.course_pk_id) \
        .filter(dbm.Session_form.status != "deleted") \
        .distinct(dbm.Session_form.days_of_week) \
        .all()

    course.teachers = [OBJ.teacher for OBJ in sub_course]
    course.session_signature = [day["days_of_week"] for day in Unique_signature]
    course.available_seat_for_subcourse = {OBJ.sub_course_pk_id: available_seat_for_subcourse(db, OBJ) for OBJ in sub_course}
    course.number_of_session = {OBJ.sub_course_pk_id: OBJ.number_of_session for OBJ in sub_course}
    course.available_seat = min([OBJ.sub_course_available_seat for OBJ in sub_course], default=0)

    return course


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse).filter(dbm.Session_form.status != "deleted").all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course).filter(dbm.Sub_Course_form.status != "deleted").all()]


def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "Bad Request: Course Not Found"

        return 200, course_additional_details(db, course)
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

        return 200, [course_additional_details(db, course) for course in courses]
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


def delete_course(db: Session, course_id, deleted_by: UUID = None):
    try:

        Course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not Course:
            return 400, "Course Not Found"

        warnings = []
        status, message = delete_subcourse(db, course_id, get_Course_active_subcourse(db, course_id))  # ignore type[call-arg]
        if status != 200:
            return status, message

        Course._Deleted_By = deleted_by
        db.delete(Course)
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

def update_course_status(db: Session, course_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).first()
        if not record:
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.update({"status": status.status_name}, synchronize_session=False)
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
