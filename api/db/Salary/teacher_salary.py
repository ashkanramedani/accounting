import dbm
import json
from datetime import date

from db.Course import SubCourse_report
from db.User_Form import *


def teacher_salary_report(db: Session, subcourse_id: UUID, DropDowns: sch.teacher_salary_DropDowns):
    try:
        status, report_summary = SubCourse_report(db, subcourse_id, DropDowns)
        return status, report_summary
    except Exception as e:
        return Return_Exception(db, e)


def teacher_courses(db: Session):
    try:
        AllCourses = db \
            .query(dbm.Course_form) \
            .order_by(dbm.Course_form.ending_date.desc()) \
            .filter(dbm.Course_form.ending_date < date.today(), dbm.Course_form.status != "deleted") \
            .all()

        return 200, AllCourses
    except Exception as e:
        return Return_Exception(db, e)


def teacher_sub_courses(db: Session, course_ID: UUID):
    try:
        if not db.query(dbm.Course_form).filter_by(course_pk_id=course_ID).filter(dbm.Course_form.status != "deleted").first():
            return 400, "Course Not Found"

        AllSubCourses = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_ID).filter(dbm.Sub_Course_form.status != "deleted").all()

        for SubCourse in AllSubCourses:
            sub_teachers: List[dbm.Session_form] = db \
                .query(dbm.Session_form) \
                .filter_by(sub_course_fk_id=SubCourse.sub_course_pk_id) \
                .filter(dbm.Session_form.status != "deleted", dbm.Session_form.session_teacher_fk_id != SubCourse.sub_course_teacher_fk_id) \
                .distinct(dbm.Session_form.session_teacher_fk_id) \
                .all()
            SubCourse.sub_teachers = [sub_teacher.teacher for sub_teacher in sub_teachers]

        return 200, AllSubCourses
    except Exception as e:
        return Return_Exception(db, e)


def number_of_sub_courses(db: Session, course_ID: UUID):
    try:
        if not db.query(dbm.Course_form).filter_by(course_pk_id=course_ID).filter(dbm.Course_form.status != "deleted").first():
            return 400, "Course Not Found"
        return 200, db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_ID).filter(dbm.Sub_Course_form.status != "deleted").count()

    except Exception as e:
        return Return_Exception(db, e)
