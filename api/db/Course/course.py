from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from ..Extra import *


def Add_tags_category(db: Session, course, course_pk_id: UUID, tags: List[sch.Update_Relation], categories: List[sch.Update_Relation]):
    Errors = []
    all_tags = [id.tag_pk_id for id in db.query(dbm.Tag_form).filter_by(deleted=False).all()]
    all_categories = [id.category_pk_id for id in db.query(dbm.Category_form).filter_by(deleted=False).all()]
    for tag in tags:
        if existing_tag := tag.old_id:
            tag_OBJ = db.query(dbm.CourseTag).filter_by(course_fk_id=course_pk_id, tag_fk_id=existing_tag, deleted=False)
            if not tag_OBJ.first():
                Errors.append(f'Course does not have this tag {existing_tag}')
            else:
                tag_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_tag := tag.new_id:
            if new_tag not in all_tags:
                Errors.append(f'this tag does not exist {new_tag}')
            else:
                course.tags.append(db.query(dbm.Tag_form).filter_by(tag_pk_id=new_tag, deleted=False).first())

    for category in categories:
        if existing_category := category.old_id:
            category_OBJ = db.query(dbm.CourseCategory).filter_by(course_fk_id=course_pk_id, category_fk_id=existing_category, deleted=False)
            if not category_OBJ.first():
                Errors.append(f'Course does not have this category {existing_category}')
            else:
                category_OBJ.update({"deleted": True}, synchronize_session=False)
        if new_category := category.new_id:
            if new_category not in all_categories:
                Errors.append(f'this category does not exist {new_category}')
            else:
                course.categories.append(db.query(dbm.Category_form).filter_by(category_pk_id=new_category, deleted=False).first())
    db.commit()
    return Errors


def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not course:
            return 400, "Bad Request: Course Not Found"
        sub_course = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id, deleted=False).all()
        if not sub_course:
            course.teachers = []
            course.session_signature = []
            course.available_seat = course.course_capacity
            return 200, course

        course.teachers = [sub_course.teacher for sub_course in sub_course]
        course.session_signature = []
        course.available_seat = min([SB.sub_course_available_seat for SB in sub_course])

        return 200, course
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_course(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        courses = record_order_by(db, dbm.Course_form, page, limit, order)
        if not courses:
            return 200, []
        Courses = []
        for course in courses:
            sub_course = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course.course_pk_id, deleted=False).all()
            if not sub_course:
                course.teachers = []
                course.session_signature = []
                course.available_seat = course.course_capacity
                Courses.append(course)
                continue

            course.teachers = [sub_course.teacher for sub_course in sub_course]
            course.session_signature = []
            course.available_seat = min([sub_course.sub_course_available_seat for sub_course in sub_course])
            Courses.append(course)

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

        tags = data.pop("tags") if "tags" in data else []
        categories = data.pop("categories") if "categories" in data else []

        OBJ = dbm.Course_form(**data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        Errors = Add_tags_category(db, OBJ, OBJ.course_pk_id, tags, categories)
        if Errors:
            return 200, "Course updated but there was an error in the tags or categories: " + ", ".join(Errors)
        return 200, "course Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_course(db: Session, course_id):
    try:
        record = db.query(dbm.Course_form).filter_by(course_pk_id=course_id, deleted=False).first()
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
        course = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_pk_id, deleted=False)
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
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

"""
update ,500,{"detail":"InvalidRequestError: ('Entity namespace for \"course_tag\" has no property \"tag_pk_id\"',)"}
"""