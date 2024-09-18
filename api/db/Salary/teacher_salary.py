import dbm
from datetime import date, timezone, timedelta, datetime
from typing import List
from sqlalchemy.orm import joinedload


from db.User_Form.Teacher_Forms import *



def teacher_courses(db: Session):
    try:
        NOW = datetime.now(tz=IRAN_TIMEZONE).date()
        AllCourses = db \
            .query(dbm.Course_form) \
            .order_by(dbm.Course_form.ending_date.desc()) \
            .filter(dbm.Course_form.ending_date < NOW, dbm.Course_form.status != "deleted") \
            .all()

        return 200, AllCourses
    except Exception as e:
        return Return_Exception(db, e)


def teacher_sub_courses(db: Session, course_ID: UUID):
    try:
        if not db.query(dbm.Course_form).filter_by(course_pk_id=course_ID).filter(dbm.Course_form.status != "deleted").first():
            return 400, "Course Not Found"

        AllSubCourses = db \
            .query(dbm.Sub_Course_form) \
            .filter_by(course_fk_id=course_ID) \
            .filter(dbm.Sub_Course_form.status != "deleted") \
            .options(joinedload(dbm.Sub_Course_form.teacher), joinedload(dbm.Sub_Course_form.course)) \
            .all()
        Existing_Salary_record_Query = db.query(dbm.Teacher_salary_form).filter(dbm.Teacher_salary_form.status != 'deleted', dbm.Teacher_salary_form.subcourse_fk_id.in_(subcourse.sub_course_pk_id for subcourse in AllSubCourses)).all()
        Existing_Salary_record_Query = [str(record.subcourse_fk_id) for record in Existing_Salary_record_Query]
        OUT: List[sch.Teacher_subcourse_report] = []
        for SubCourse in AllSubCourses:
            sub_teachers: List[dbm.Session_form] = db \
                .query(dbm.Session_form) \
                .filter_by(sub_course_fk_id=SubCourse.sub_course_pk_id) \
                .filter(dbm.Session_form.status != "deleted", dbm.Session_form.session_teacher_fk_id != SubCourse.sub_course_teacher_fk_id) \
                .distinct(dbm.Session_form.session_teacher_fk_id) \
                .all()
            SubCourse.sub_teachers = [sub_teacher.teacher for sub_teacher in sub_teachers]
            RECORD = sch.Teacher_subcourse_report(**SubCourse.__dict__)
            RECORD.Does_Have_Salary_Record = str(SubCourse.sub_course_pk_id) in Existing_Salary_record_Query
            OUT.append(RECORD)
        return 200, OUT
    except Exception as e:
        return Return_Exception(db, e)


def number_of_sub_courses(db: Session, course_ID: UUID):
    try:
        if not db.query(dbm.Course_form).filter_by(course_pk_id=course_ID).filter(dbm.Course_form.status != "deleted").first():
            return 400, "Course Not Found"
        return 200, db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_ID).filter(dbm.Sub_Course_form.status != "deleted").count()

    except Exception as e:
        return Return_Exception(db, e)
