from typing import List, Dict, Tuple, Union, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from db.Extra import *
from lib import DEV_io, logger
from schemas import course_data_for_report

Base_salary = {Cap: {"OnSite": 77, "online": 66, "hybrid": 0} for Cap in ["1-5", "6-9", "10-12", "13"]}
TEACHER_TARDY = {"0_10": 11, "10_30": 5.5, "30_40": -5.5, "40": -16.5}
COURSE_LEVEL = {"connect": 11, "FCE": 22, "CAE": 44, "CPE": 66}
SCORES = {
    "effect_on_total": ["loan", "reward", "punishment", "cancelled_session_score"],
    "effect_on_session": ["content_creation", "event_participate", "CPD", "Odd_hours", "report_to_student", "LP_submission", "student_assign_feedback", "survey_score", "result_submission_to_FD", "roles_score", "tardy_score", "course_level_score"]
}
DropDown_value_table = {
    "report_to_student": {"weak": -5.5, "average": 0, "good": 5.5, "excellent": 11},
    "LP_submission": {"weak": -11, "average": 5.5, "good": 11, "excellent": 16.5},
    "student_assign_feedback": {"weak": -5.5, "average": 0, "good": 5.5, "excellent": 11},
    "survey_score": {"weak": 0, "average": 3, "good": 6, "excellent": 10},
    "result_submission_to_FD": {"weak": -5.5, "average": 0, "good": 5.5}
}


def Tardy_Score(tardy: int):
    match tardy:
        case x if x <= 10:
            return TEACHER_TARDY["0_10"]
        case x if 10 <= x <= 30:
            return TEACHER_TARDY["10_30"]
        case x if 30 <= x <= 40:
            return TEACHER_TARDY["30_40"]
        case x if 40 <= x:
            return TEACHER_TARDY["40"]


def PreProcess_teacher_report(db: Session, sub_course_obj: dbm.Sub_Course_form) -> tuple[int, str | dict[str, sch.Report]]:
    """Fetches and processes report data for a sub-course.

    Args:
        db: SQLAlchemy session object.
        sub_course_obj: Pydantic model representing the sub-course.

    Returns:
        An HTTP status code and either an error message (on failure)
        or a dictionary containing teacher reports (on success).
    """

    # Combine queries using a JOIN and filtering
    teachers_query = db.query(dbm.User_form) \
        .join(dbm.Session_form, dbm.Session_form.session_teacher_fk_id == dbm.User_form.user_pk_id) \
        .filter(
            dbm.Session_form.sub_course_fk_id == sub_course_obj.sub_course_pk_id,
            dbm.Session_form.status != "deleted", dbm.User_form.status != "deleted") \
        .options(joinedload(dbm.User_form.roles)) \
        .all()

    return 200, {
        str(teacher.user_pk_id): sch.Report(**teacher.__dict__, SUB=teacher.user_pk_id != sub_course_obj.sub_course_teacher_fk_id)
        for teacher in teachers_query
    }

def Apply_scores(
        DropDowns: sch.teacher_salary_DropDowns,
        sub_course_summary: dict[str, sch.Report],
        course_level: str,
        subcourse_teacher: UUID) -> List:

    Final = []
    Score = {
        field: value
        if isinstance(value, float) else DropDown_value_table[field][value.value]
        for field, value in DropDowns
    }
    Score["course_level_score"] = COURSE_LEVEL.get(course_level, 0)

    data = sub_course_summary[str(subcourse_teacher)]
    Score["tardy_score"] = Tardy_Score(data.tardy)
    Score["cancellation_factor"] *= data.cancelled_session

    effect_on_session = sum([value for key, value in Score.items() if key in SCORES["effect_on_session"]])

    for teacher_id, data in sub_course_summary.items():
        Total_session = data.attended_session + data.sub_point
        data.score = effect_on_session + data.roles_score
        data.earning = Total_session * effect_on_session
        percentage = min(100, (data.ID_Experience // 36000) * 2)
        data.earning += ((data.earning * percentage) / 100)

        Final.append({**data.__dict__, **Score, "user_fk_id": teacher_id})

    # Final["score"] = Score
    return Final


@DEV_io()
def SubCourse_report(db: Session, sub_course_id: UUID, DropDowns: sch.teacher_salary_DropDowns) -> Tuple[int, List[dbm.Teacher_salary_form] | str]:
    sub_course: dbm.Sub_Course_form = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=sub_course_id).first()

    Existing_salary = db.query(dbm.Teacher_salary_form).filter_by(subcourse_fk_id=sub_course.sub_course_pk_id).all()
    if Existing_salary:
        return 200, Existing_salary

    if not sub_course:
        return 400, "sub course not found"

    course_data = db.query(dbm.Course_form) \
        .filter_by(course_pk_id=sub_course.course_fk_id) \
        .filter(dbm.Course_form.status != "deleted") \
        .options(joinedload(dbm.Course_form.type), joinedload(dbm.Course_form.language)) \
        .first()

    try:
        course_data = course_data.__dict__
    except AttributeError:
        return 400, f"Course data Could Not loaded"

    course_data = sch.course_data_for_report(**course_data)

    if course_data.BaseSalary is None:
        return 400, f"No BaseSalary Found for {sub_course.sub_course_name}. ({course_data.course_capacity}, {course_data.course_type})"

    status, sub_course_summary = PreProcess_teacher_report(db, sub_course)
    if status != 200:
        return status, sub_course_summary

    # Loop Through Sessions
    for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=sub_course.sub_course_pk_id).filter(dbm.Session_form.status != "deleted").all():
        Session_teacher = str(session.session_teacher_fk_id)
        if Session_teacher not in sub_course_summary:
            logger.warning(f"Teacher: {Session_teacher} Has Been Skipped. ")
            continue

        if session.canceled:  # or not session.report:  # NC: 001
            if not sub_course_summary[Session_teacher].SUB:
                sub_course_summary[Session_teacher].cancelled_session += 1

        elif session.is_sub:
            sub_request = db \
                .query(dbm.Sub_Request_form) \
                .filter(dbm.Sub_Request_form.sub_request_pk_id == session.sub_Request, dbm.Sub_Request_form.status != "deleted") \
                .first()

            sub_course_summary[str(sub_request.main_teacher_fk_id)].sub_point -= 1
            sub_course_summary[str(sub_request.sub_teacher_fk_id)].sub_point += 2
        else:
            sub_course_summary[Session_teacher].attended_session += 1
            sub_course_summary[Session_teacher].experience_gain += session.session_duration

    # Calculate the Tardy for Each Teacher
    Tardies: List[dbm.Teacher_Tardy_report_form] = db \
        .query(dbm.Teacher_Tardy_report_form) \
        .filter_by(sub_course_fk_id=sub_course.sub_course_pk_id, teacher_fk_id=sub_course.sub_course_teacher_fk_id) \
        .filter(dbm.Teacher_Tardy_report_form.status != "deleted").all()

    for tardy in Tardies:
        sub_course_summary[str(tardy.teacher_fk_id)].tardy += tardy.delay

    OBJs = []
    teacher_salary_records = Apply_scores(DropDowns, sub_course_summary, course_data.course_level, sub_course.sub_course_teacher_fk_id)
    for salary_record in teacher_salary_records:
        OBJs.append(dbm.Teacher_salary_form(**salary_record, subcourse_fk_id=sub_course.sub_course_pk_id, BaseSalary=course_data.BaseSalary))  # type: ignore[call-arg]
        User_obj = db.query(dbm.User_form).filter_by(user_pk_id=salary_record["user_fk_id"]).first()
        User_obj.ID_Experience += salary_record["experience_gain"]

    db.add_all(OBJs)
    db.commit()

    return 200, db.query(dbm.Teacher_salary_form).filter_by(subcourse_fk_id=sub_course.sub_course_pk_id).all()


def update_SubCourse_report(db: Session, form_ID: UUID, Form: sch.update_salary_report):
    Salary_record = db \
        .query(dbm.Teacher_salary_form) \
        .filter_by(teacher_salary_pk_id=form_ID) \
        .filter(dbm.Teacher_salary_form.status != "deleted") \
        .first()

    Salary_record.rewards_earning = Form.rewards_earning
    Salary_record.punishment_deductions = Form.punishment_deductions
    Salary_record.loan_installment = Form.loan_installment

    Salary_record.earning += (Form.rewards_earning - Form.punishment_deductions - Form.loan_installment)

    Salary_record.payment = Form.payment
    Salary_record.payment_date = Form.payment_date
    db.commit()
    return 200
