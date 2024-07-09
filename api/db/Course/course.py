from typing import List, Dict
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .sub_course import delete_subcourse
from ..Extra import *


def get_subCourse_active_session(db: Session, SubCourse: UUID) -> List[UUID]:
    return [session.session_pk_id for session in db.query(dbm.Session_form).filter_by(sub_course_fk_id=SubCourse).filter(dbm.Session_form.status != "deleted").all()]


def get_Course_active_subcourse(db: Session, Course: UUID) -> List[UUID]:
    return [subcourse.sub_course_pk_id for subcourse in db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Course).filter(dbm.Sub_Course_form.status != "deleted").all()]


def get_course(db: Session, course_id):
    try:
        course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").first()
        if not course:
            return 400, "Bad Request: Course Not Found"
        sub_course = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course_id).filter(dbm.Sub_Course_form.status != "deleted").all()
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
        return Return_Exception(db, e)


def get_all_course(db: Session, course_type: str | None, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        if course_type:
            Course_type = db.query(dbm.Course_Type_form).filter_by(course_type_name=course_type).first().course_type_pk_id
            if Course_type:
                courses = record_order_by(db, dbm.Course_form, page, limit, order, course_type=Course_type)
            else:
                courses = []
        else:
            courses = record_order_by(db, dbm.Course_form, page, limit, order)
        if not courses:
            return 200, []
        Courses = []
        for course in courses:
            sub_course: List[dbm.Sub_Course_form] = db.query(dbm.Sub_Course_form).filter_by(course_fk_id=course.course_pk_id).filter(dbm.Sub_Course_form.status != "deleted").all()

            if not sub_course:
                course.teachers = []
                course.session_signature = []
                course.available_seat = course.course_capacity
                Courses.append(course)
                continue

            course.teachers = [OBJ.teacher for OBJ in sub_course]
            course.course_signature = db.query(dbm.Session_form.days_of_week, dbm.Session_form.session_date).filter_by(course_fk_id=course.course_pk_id).filter(dbm.Session_form.status != "deleted").distinct().all()

            course.available_seat = min([OBJ.sub_course_available_seat for OBJ in sub_course])
            Courses.append(course)

        return 200, Courses
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


def delete_course(db: Session, course_id):
    try:

        Course = db.query(dbm.Course_form).filter_by(course_pk_id=course_id).filter(dbm.Course_form.status != "deleted").filter(dbm.Base_form.status).first()
        if not Course:
            return 400, "Course Not Found"

        warnings = []
        status, message = delete_subcourse(db, course_id, get_Course_active_subcourse(db, course_id))  # ignore type[call-arg]
        if status != 200:
            return status, message
        Course.deleted = True
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


Base_salary = {
    "1-5": {"in_person": 77, "online": 66, "hybrid": 0, "Not_Assigned": 0},
    "6-9": {"in_person": 77, "online": 66, "hybrid": 0, "Not_Assigned": 0},
    "10-12": {"in_person": 77, "online": 66, "hybrid": 0, "Not_Assigned": 0},
    "13": {"in_person": 77, "online": 66, "hybrid": 0, "Not_Assigned": 0}}

TEACHER_TARDY = {"0_10": 11, "10_30": 5.5, "30_40": -5.5, "40": -16.5}
TEACHER_LEVEL = {"regular": 0, "expert": 22, "visiting: 0, guest": 0, "exam: 30, test": 30, "master": 40, "supervisor": 55, "master_supervisor": 5.5, "director_of_education": 5.5}
COURSE_LEVEL = {"connect": 11, "FCE": 22, "CAE": 44, "CPE": 66}


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
                "Teacher_Level_Score": TEACHER_LEVEL.get(Teacher_Level.lower(), 0),
                "Tardy": Tardy,
                "Tardy_Score": Tardy_Score(Tardy),
                "Course_Level": course_level,
                "Course_Level_Score": COURSE_LEVEL.get(course_level.lower(), 0)
            })
        else:
            new_sub_course_summary[field] = record
    return new_sub_course_summary


def course_report(db, course_id: UUID, Cancellation_factor):
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
