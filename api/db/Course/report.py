import json
from typing import List, Dict
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
from db.Extra import *
from lib import DEV_io, logger

Base_salary = {Cap: {"in_person": 77, "online": 66, "hybrid": 0, "Not_Assigned": 0} for Cap in ["1-5", "6-9", "10-12", "13"]}
TEACHER_TARDY = {"0_10": 11, "10_30": 5.5, "30_40": -5.5, "40": -16.5}
TEACHER_LEVEL = {"regular": 0, "expert": 22, "visiting: 0, guest": 0, "exam: 30, test": 30, "master": 40, "supervisor": 55, "master_supervisor": 5.5, "director_of_education": 5.5}
COURSE_LEVEL = {"connect": 11, "FCE": 22, "CAE": 44, "CPE": 66}

def Get_Teacher_Level_Score(level: str):
    if not level:
        return 0
    else:
        return TEACHER_LEVEL.get(level.lower(), 0)

def Get_Course_Level_Score(level: str):
    if not level:
        return 0
    else:
        return COURSE_LEVEL.get(level.lower(), 0)

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


def safe_field(db: Session, Data: Dict, *fields: UUID | str) -> Dict[str, Dict]:
    """Safely add a fields to given dict if not exist"""
    for teacher_id in fields:
        if str(teacher_id) not in Data:
            Data[f'{teacher_id}'] = {
                "Teacher_Level": db.query(dbm.User_form).filter_by(user_pk_id=teacher_id).filter(dbm.User_form.status != "deleted").first().level,
                "Attended_Session": 0,
                "Cancelled_Session": 0,
                "Sub_point": 0,
                "Tardy": 0}
    return Data


@DEV_io()
def SubCourse_report(db: Session, sub_course: dbm.Sub_Course_form, course_level: str, course_type: dbm.Course_Type_form, Cancellation_factor: float) -> Dict | str:
    BaseSalary_for_course_type = BaseSalary_for_SubCourse(sub_course.sub_course_capacity, course_type.course_type_name)  # Code: 001
    if BaseSalary_for_course_type is None:
        return f"No BaseSalary Found for SubCourse: {sub_course.sub_course_name}. "

    sub_course_summary: Dict = {"BaseSalary": BaseSalary_for_course_type, "course_level": course_level}

    sub_course_Sessions: List[dbm.Session_form] = db.query(dbm.Session_form).filter_by(sub_course_fk_id=sub_course.sub_course_pk_id).filter(dbm.Session_form.status != "deleted").all()
    if not sub_course_Sessions:
        return f"{sub_course.sub_course_name} has no sessions. "

    # Loop Through Sessions
    for session in sub_course_Sessions:
        Session_teacher = str(session.session_teacher_fk_id)
        sub_course_summary = safe_field(db, sub_course_summary, Session_teacher)

        if session.canceled:  # or not session.report:  # NC: 001
            sub_course_summary[Session_teacher]["Cancelled_Session"] += 1

        elif session.is_sub:
            sub_request: dbm.Sub_Request_form = db.query(dbm.Sub_Request_form).filter_by(sub_request_pk_id=session.sub_Request).filter(dbm.Sub_Request_form.status != "deleted").first()
            main_teacher, sub_teacher = str(sub_request.main_teacher_fk_id), str(sub_request.sub_teacher_fk_id)
            sub_course_summary = safe_field(db, sub_course_summary, main_teacher, sub_teacher)
            sub_course_summary[main_teacher]["Sub_point"] -= 1
            sub_course_summary[sub_teacher]["Sub_point"] += 2
        else:
            sub_course_summary[Session_teacher]["Attended_Session"] += 1

    # Calculate the Tardy for Each Teacher
    for tardy in db.query(dbm.Teacher_Tardy_report_form).filter_by(course_fk_id=sub_course.course_fk_id, sub_course_fk_id=sub_course.sub_course_pk_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").all():
        sub_course_summary[f"{tardy.teacher_fk_id}"]["Tardy"] += tardy.delay

    # Calculate Cancellation/Tardy Score

    Users_OBJ = db.query(dbm.User_form).filter(dbm.User_form.status != "deleted").filter(dbm.User_form.user_pk_id.in_([UID for UID, Data in sub_course_summary.items() if isinstance(Data, dict)])).all()
    Users = {str(user.user_pk_id): f'{user.name} {user.last_name}' for user in Users_OBJ}

    # Calculate Scores
    new_sub_course_summary = {"Teacher": []}
    for field, record in sub_course_summary.items():
        if isinstance(record, dict):
            Tardy: int = record.pop("Tardy")
            Teacher_Level: str = record["Teacher_Level"]
            Cancelled_Session: int = record.pop("Cancelled_Session")

            new_sub_course_summary["Teacher"].append({
                "teacher_id": field,
                "teacher_name": Users[field],
                "Attended_Session": record["Attended_Session"],
                "Cancelled_Session": Cancelled_Session,
                "Cancelled_Session_Score": Cancelled_Session * Cancellation_factor,
                "Teacher_Level": Teacher_Level,
                "Teacher_Level_Score": Get_Teacher_Level_Score(Teacher_Level),
                "Tardy": Tardy,
                "Tardy_Score": Tardy_Score(Tardy),
                "Course_Level": course_level,
                "Course_Level_Score": Get_Course_Level_Score(course_level)
            })
        else:
            new_sub_course_summary[field] = record
    return new_sub_course_summary


@DEV_io()
def course_report_summary(db: Session, course_id: UUID, Cancellation_factor: int):
    try:
        Course_summary = {}
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "No Course with these id Found"

        sub_courses: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id).filter(dbm.Sub_Course_form.status != "deleted")
        if not sub_courses:
            return 400, "No Sub Course Found in Given Course"

        course_level = course.course_level
        course_type = db.query(dbm.Course_Type_form).filter_by(course_type_pk_id=course.course_type).filter(dbm.Course_Type_form.status != "deleted").first()
        # Loop Through SubCourse
        for sub_course in sub_courses:
            Course_summary[f"{sub_course.sub_course_name}"] = SubCourse_report(db, sub_course, course_level, course_type, Cancellation_factor)

        return 200, Course_summary
    except Exception as e:
        return Return_Exception(db, e)
