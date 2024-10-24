from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from api.db.Course import course_additional_details
from db.Extra import *


def get_sign_up_active_course(db: Session, course_id: UUID):
    Courses = db \
        .query(dbm.Course_form) \
        .filter_by(course_pk_id=course_id) \
        .filter(
            dbm.Course_form.status != "deleted",
            dbm.Course_form.starting_date < datetime.now(tz=IRAN_TIMEZONE).date()) \
        .all()

    return [course_additional_details(db, course) for course in Courses]


def get_sign_up_active_subcourse(db: Session, sub_course_id: UUID):
    return db \
        .query(dbm.Sub_Course_form) \
        .filter_by(sub_course_pk_id=sub_course_id) \
        .filter(
            dbm.Sub_Course_form.status != "deleted",
            dbm.Sub_Course_form.sub_course_starting_date < datetime.now(tz=IRAN_TIMEZONE).date()) \
        .all()


def pre_payment_sign_up(db: Session, Form: sch.post_pre_payment_sign_up):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_id).first()
        if course is None:
            return 404, "Course Not Found"
        if Form.sub_course_ids:
            package_discount = 0
            sub_courses: List[dbm.Sub_Course_form] = [db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=sub_course_id).first() for sub_course_id in Form.sub_course_ids]
            if sub_courses is None:
                return 404, "Sub Course Not Found"
        else:
            package_discount = course.package_discount
            sub_courses: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Form.course_id).all()
            if sub_courses is None:
                return 404, "Sub Course Not Found"

        ready_to_signup = []
        total_price = 0
        for sub_course in sub_courses:
            singUps = sum(db.query(TBL).filter_by(subcourse_fk_id=sub_course.sub_course_pk_id, student_pk_id=Form.student_pk_id).count() for TBL in [dbm.SignUp_queue, dbm.SignUp_queue])

            if singUps >= course.sub_course_capacity:
                return 400, f"Sub_Course is Full: {sub_course.sub_course_name}"

            ready_to_signup.append({"course_fk_id": course.course_pk_id, "subcourse_fk_id": sub_course.sub_course_pk_id, "student_pk_id": Form.student_pk_id})
            total_price += sub_course.sub_course_price

        fix_discount = 0
        percentage_discount = 0
        discount_code = None
        if Form.discount_code:
            discount_code = db.query(dbm.Discount_code_form).filter_by(discount_code=Form.discount_code).first()
            if discount_code.discount_type == "percentage":
                percentage_discount = discount_code.discount_value
            else:
                fix_discount = discount_code.discount_value

        db.add_all([dbm.SignUp_queue(**sub_course) for sub_course in ready_to_signup])

        discount_price = (total_price - ((total_price * (package_discount + percentage_discount)) / 100)) - fix_discount

        SignUp_payment = dbm.SignUp_payment_queue_form(student_pk_id=Form.student_pk_id, course_fk_id=Form.course_id, discount_code=discount_code.discount_code_pk_id, total_price=total_price, discount_price=discount_price, package_discount=package_discount)  # type: ignore[call-arg]

        db.add(SignUp_payment)
        db.commit()
        db.flush()

        return 200, SignUp_payment

    except Exception as e:
        return Return_Exception(db, e)


def sign_up(db: Session, success: bool, pre_payment_id: UUID):
    if not success:
        return 400, "Payment Failed"

    payment_record: dbm.SignUp_payment_queue_form = db.query(dbm.SignUp_payment_queue_form).filter_by(signup_queue_pk_id=pre_payment_id).first()
    payment_record.status = "payed"
    all_sign_up: List[dbm.SignUp_queue] = db.query(dbm.SignUp_queue).filter_by(course_fk_id=payment_record.course_fk_id, student_pk_id=payment_record.student_pk_id).all()

    for signup in all_sign_up:
        dbm.SignUp_form(student_pk_id=payment_record.student_pk_id, course_fk_id=payment_record.course_fk_id, subcourse_fk_id=signup.subcourse_fk_id)
        db.delete(signup)
    db.commit()

    return 200, payment_record
