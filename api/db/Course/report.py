from typing import List, Dict, Tuple, Union, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from db.Extra import *
from lib import DEV_io, logger
from schemas import course_data_for_report

Base_salary = {Cap: {"OnSite": 770_000, "online": 660_000, "hybrid": 0} for Cap in ["1-5", "6-9", "10-12", "13"]}
TEACHER_TARDY = {"0_10": 110_000, "10_30": 55_000, "30_40": -55_000, "40": -165_000}
COURSE_LEVEL = {"connect": 110_000, "FCE": 220_000, "CAE": 440_000, "CPE": 660_000}
SCORES = {
    "effect_on_total": ["loan", "reward", "punishment", "cancelled_session_score"],
    "Percent_on_session": ["content_creation", "event_participate", "CPD", "Odd_hours"],
    "effect_on_session": ["report_to_student", "LP_submission", "student_assign_feedback", "x", "result_submission_to_FD", "course_level_score", "BaseSalary"]
}
DropDown_value_table = {
    "report_to_student": {"weak": -55_000, "average": 0, "good": 55_000, "excellent": 110_000},
    "LP_submission": {"weak": -110_000, "average": 55_000, "good": 110_000, "excellent": 165_000},
    "student_assign_feedback": {"weak": -55_000, "average": 0, "good": 55_000, "excellent": 110_000},
    "survey_score": {"weak": 0, "average": 30_000, "good": 60_000, "excellent": 100_000},
    "result_submission_to_FD": {"weak": -55_000, "average": 0, "good": 55_000}
}


def BaseSalary_for_SubCourse(course_cap: int, course_type: str):
    try:
        match course_cap:
            case x if x <= 5:
                return Base_salary["1-5"][course_type]
            case x if 6 <= x <= 9:
                return Base_salary["6-9"][course_type]
            case x if 10 <= x <= 12:
                return Base_salary["10-12"][course_type]
            case x if 13 <= x:
                return Base_salary["13"][course_type]
    except KeyError:
        return None


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
    teachers_query = db.query(dbm.User_form) \
        .join(dbm.Session_form, dbm.Session_form.session_teacher_fk_id == dbm.User_form.user_pk_id) \
        .filter(dbm.Session_form.sub_course_fk_id == sub_course_obj.sub_course_pk_id, dbm.Session_form.status != "deleted", dbm.User_form.status != "deleted") \
        .options(joinedload(dbm.User_form.roles)) \
        .all()

    return 200, {
        str(teacher.user_pk_id): sch.Report(**teacher.__dict__, SUB=teacher.user_pk_id != sub_course_obj.sub_course_teacher_fk_id)
        for teacher in teachers_query
    }


@DEV_io()
def Apply_scores(DropDowns: sch.teacher_salary_DropDowns, sub_course_summary: dict[str, sch.Report], course_data: sch.course_data_for_report) -> List[Dict]:
    Final = []
    Score = {
        field: DropDown_value_table[field][value.value]
        if field in DropDown_value_table.keys() else value
        for field, value in DropDowns
    }
    cancellation_factor = Score.pop("cancellation_factor")

    Score["course_level_score"] = COURSE_LEVEL.get(course_data.course_level, 0)
    Score["BaseSalary"] = BaseSalary_for_SubCourse(course_data.course_capacity, course_data.course_type)

    Base_Session_score = sum([value for key, value in Score.items() if key in SCORES["effect_on_session"]])

    percent_on_session = {
        key: (Base_Session_score * value) / 100
        for key, value in Score.items()
        if key in SCORES["Percent_on_session"]}

    percent_on_session_score = sum(percent_on_session.values())

    for teacher_id, data in sub_course_summary.items():
        data.ID_Experience = min(60, (data.ID_Experience // 36_000) * 2)
        teacher_base_score = Base_Session_score + ((Base_Session_score * data.ID_Experience) / 100) + percent_on_session_score + Tardy_Score(data.tardy) + data.roles_score

        session_cancellation_deduction = cancellation_factor * Base_Session_score * data.cancelled_session

        earning = ((data.attended_session + data.sub_point) * teacher_base_score) - session_cancellation_deduction

        Final.append({
            **Score,
            **data.__dict__,
            **percent_on_session,
            "earning": earning,
            "user_fk_id": teacher_id,
            "score": teacher_base_score,
            "session_cancellation_deduction": session_cancellation_deduction})
    return Final


@DEV_io()
def SubCourse_report(db: Session, sub_course_id: UUID, DropDowns: sch.teacher_salary_DropDowns):
    sub_course: dbm.Sub_Course_form = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=sub_course_id).first()

    if not sub_course:
        return 400, "sub course not found"

    Existing_salary = db.query(dbm.Teacher_salary_form).filter_by(subcourse_fk_id=sub_course.sub_course_pk_id).all()
    if Existing_salary:
        return 200, Existing_salary

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

    status, sub_course_summary = PreProcess_teacher_report(db, sub_course)
    if status != 200:
        return status, sub_course_summary

    # Loop Through Sessions
    AllSessions = db.query(dbm.Session_form).filter_by(sub_course_fk_id=sub_course.sub_course_pk_id).filter(dbm.Session_form.status != "deleted").all()
    sub_course_summary[str(sub_course.sub_course_teacher_fk_id)].total_sessions = len(AllSessions)
    for session in AllSessions:
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

    OBJs: List[dbm.Teacher_salary_form] = []
    teacher_salary_records = Apply_scores(DropDowns, sub_course_summary, course_data, sub_course.sub_course_teacher_fk_id)

    Extra = {"subcourse_fk_id": sub_course.sub_course_pk_id, "course_data": course_data.__dict__}
    for salary_record in teacher_salary_records:
        OBJ = dbm.Teacher_salary_form(**salary_record, **Extra)  # type: ignore[call-arg]

        User_obj = db.query(dbm.User_form).filter_by(user_pk_id=salary_record["user_fk_id"]).first()
        User_obj.ID_Experience += salary_record["experience_gain"] + 10_000_000
        OBJs.append(OBJ)

    db.add_all(OBJs)
    db.commit()
    # return 200, OBJs
    return 200, db \
        .query(dbm.Teacher_salary_form) \
        .filter_by(subcourse_fk_id=sub_course.sub_course_pk_id) \
        .options(
            joinedload(dbm.Teacher_salary_form.teacher),
            joinedload(dbm.Teacher_salary_form.card),
            joinedload(dbm.Teacher_salary_form.sub_course)) \
        .all()


def update_SubCourse_report(db: Session, form_ID: UUID, Form: sch.update_salary_report):
    try:
        existing = db \
            .query(dbm.Teacher_salary_form) \
            .filter_by(teacher_salary_pk_id=form_ID) \
            .filter(dbm.Teacher_salary_form.status != "deleted")

        salary_data = existing.first()
        if not salary_data:
            return 400, "Bad Request: Target salary record not found"

        changes = {**Form.__dict__, "earning": salary_data.earning + (Form.rewards_earning - Form.punishment_deductions - Form.loan_installment)}

        existing.update({**changes}, synchronize_session=False)
        db.commit()
        return 200, existing.first()

    except Exception as e:
        return Return_Exception(db, e)
