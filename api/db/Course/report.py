from typing import List, Dict, Tuple, Union
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from db.Extra import *
from lib import DEV_io, logger

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



@DEV_io()
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


def Empty_report(teacher: dbm.User_form, **Field) -> Dict:
    if Field["SUB"]:
        return {"SUB": Field["SUB"], "sub_point": 0, "name": f'{teacher.name} {teacher.last_name}'}
    return {
        **Field,
        "tardy": 0,
        "sub_point": 0,
        "experience_gain": 0,
        "attended_session": 0,
        "cancelled_session": 0,
        "name": f'{teacher.name} {teacher.last_name}',
        "roles_score": sum(i.value for i in teacher.roles) if teacher.roles else 0,
        "roles": {f'{i.cluster}_{i.name}': i.value for i in teacher.roles} if teacher.roles else {},
    }

def PreProcess_report2(db: Session, sub_course_obj: dbm.Sub_Course_form):
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


    course_data_Query = db.query(dbm.Course_form) \
        .filter_by(course_pk_id=sub_course_obj.course_fk_id) \
        .filter(dbm.Course_form.status != "deleted") \
        .options(joinedload(dbm.Course_form.type)) \
        .options(joinedload(dbm.Course_form.language)) \
        .first()

    if not course_data_Query:
        return 400, "Course Not load course data"

    course_data = sch.course_data_for_report(**course_data_Query.__dict__)

    if course_data.BaseSalary is None:
        return 400, f"No BaseSalary Found for {sub_course_obj.sub_course_name}. ({course_data.course_capacity}, {course_data.course_type})"

    return 200, {
        str(teacher.user_pk_id): Empty_report(
                teacher,
                **course_data.dict(),
                SUB=teacher.user_pk_id != sub_course_obj.sub_course_teacher_fk_id)
        for teacher in teachers_query}


def PreProcess_report(db: Session, sub_course_obj: dbm.Sub_Course_form):
    # NC: 009 & NC: (add i.cluster == "Teacher" if needed)
    Unique_Teacher_on_course = db \
        .query(dbm.Session_form.session_teacher_fk_id) \
        .filter(
            dbm.Session_form.sub_course_fk_id == sub_course_obj.sub_course_pk_id,
            dbm.Session_form.status != "deleted") \
        .distinct() \
        .all()

    level_Query: List[dbm.User_form] = db \
        .query(dbm.User_form) \
        .options(joinedload(dbm.User_form.roles)) \
        .filter(dbm.User_form.user_pk_id.in_([teacher[0] for teacher in Unique_Teacher_on_course]), dbm.User_form.status != "deleted") \
        .all()

    course_data_Query = db \
        .query(dbm.Course_form) \
        .filter_by(course_pk_id=sub_course_obj.course_fk_id) \
        .options(joinedload(dbm.Course_form.type)) \
        .first()

    if not course_data_Query:
        return 400, "Course Not load course data"

    course_data = sch.course_data_for_report(**course_data_Query.__dict__)

    if course_data.BaseSalary is None:
        return 400, f"No BaseSalary Found for {sub_course_obj.sub_course_name}. ({course_data.course_capacity}, {course_data.course_type})"

    return 200, {
        str(teacher.user_pk_id): Empty_report(
                teacher,
                **course_data.__dict__,
                SUB=teacher.user_pk_id != sub_course_obj.sub_course_teacher_fk_id)
        for teacher in level_Query
    }

def Apply_scores(DropDowns: Dict, sub_course_summary: Dict):
    Score = {
        field: value if isinstance(value, float) else DropDown_value_table[field][value.value]
        for field, value in DropDowns.items()
    }

    for teacher, data in sub_course_summary.items():
        if not sub_course_summary[teacher]["SUB"]:
            Score["roles_score"] = data.pop("roles_score", 0)
            Score["tardy_score"] = Tardy_Score(data["tardy"])
            Score["course_level_score"] = COURSE_LEVEL.get(data["course_level"] if data["course_level"] else '', 0)
            Score["cancellation_factor"] *= data["cancelled_session"]
            break

    effect_on_session = sum([value for key, value in Score.items() if key in SCORES["effect_on_session"]])
    Score["effect_on_total"] = Score["reward"] - Score["loan"] - Score["punishment"]

    for teacher_id, data in sub_course_summary.items():
        Total_session = data.get("attended_session", 0) + data.get("sub_point", 0)
        data["score"] = effect_on_session
        data["earning"] = Total_session * effect_on_session

    sub_course_summary["score"] = Score
    return sub_course_summary

@DEV_io()
def SubCourse_report(db: Session, sub_course_id: UUID, DropDowns: sch.teacher_salary_DropDowns) -> Tuple[int, Dict | str]:
    sub_course: dbm.Sub_Course_form = db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=sub_course_id).first()

    if not sub_course:
        return 400, "sub course not found"

    # status, sub_course_summary = PreProcess_report(db, sub_course)
    status, sub_course_summary = PreProcess_report2(db, sub_course)
    if status != 200:
        return status, sub_course_summary

    # Loop Through Sessions
    for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=sub_course.sub_course_pk_id).filter(dbm.Session_form.status != "deleted").all():
        Session_teacher = str(session.session_teacher_fk_id)
        if Session_teacher not in sub_course_summary:
            logger.warning(f"Teacher: {Session_teacher} Has Been Skipped. ")
            continue

        if session.canceled:  # or not session.report:  # NC: 001
            if not sub_course_summary[Session_teacher]["SUB"]:
                sub_course_summary[Session_teacher]["cancelled_session"] += 1

        elif session.is_sub:
            sub_request = db \
                .query(dbm.Sub_Request_form) \
                .filter(dbm.Sub_Request_form.sub_request_pk_id == session.sub_Request, dbm.Sub_Request_form.status != "deleted") \
                .first()

            sub_course_summary[str(sub_request.main_teacher_fk_id)]["sub_point"] -= 1
            sub_course_summary[str(sub_request.sub_teacher_fk_id)]["sub_point"] += 2
        else:
            sub_course_summary[Session_teacher]["attended_session"] += 1
            sub_course_summary[Session_teacher]["experience_gain"] += session.session_duration


    # Calculate the Tardy for Each Teacher
    Tardies: List[dbm.Teacher_Tardy_report_form] = db \
        .query(dbm.Teacher_Tardy_report_form) \
        .filter_by(sub_course_fk_id=sub_course.sub_course_pk_id, teacher_fk_id=sub_course.sub_course_teacher_fk_id) \
        .filter(dbm.Teacher_Tardy_report_form.status != "deleted").all()

    for tardy in Tardies:
        sub_course_summary[str(tardy.teacher_fk_id)]["tardy"] += tardy.delay

    return 200, Apply_scores(DropDowns.__dict__, sub_course_summary)


@DEV_io()
def course_report_summary(db: Session, course_id: UUID, main_DropDown: sch.teacher_salary_DropDowns):
    try:
        Course_summary = {}
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "No Course with these id Found"

        sub_courses: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id).filter(dbm.Sub_Course_form.status != "deleted")
        if not sub_courses:
            return 400, "No Sub Course Found in Given Course"

        # Loop Through SubCourse
        for sub_course in sub_courses:
            Course_summary[f"{sub_course.sub_course_name}"] = SubCourse_report(db, sub_course.sub_course_pk_id, main_DropDown)
            # break

        return 200, Course_summary
    except Exception as e:
        return Return_Exception(db, e)
