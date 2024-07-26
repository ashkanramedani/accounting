import dbm
import json
from datetime import date

from db.Course import course_report
from db.User_Form import *

def teacher_salary_report(db: Session, Form: sch.teacher_salary_report):
    try:
        status, report_summary = course_report(db, Form.course_id, Form.Cancellation_factor)
        return status, report_summary
    except Exception as e:
        return Return_Exception(db, e)


def teacher_salary(db: Session):
    try:
        AllCourses = db \
            .query(dbm.Course_form) \
            .filter(dbm.Course_form.ending_date < date.today(), dbm.Course_form.status != "deleted") \
            .order_by(dbm.Course_form.ending_date.desc()) \
            .all()
        return 200, AllCourses
    except Exception as e:
        return Return_Exception(db, e)
