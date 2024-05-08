from typing import List

from lib import API_Exception
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/teacher_payment', tags=['Remote Request'])

Base_salary = {
    "1-5": {"in_person": 77, "online": 66, "hybrid": 0},
    "6-9": {"in_person": 77, "online": 66, "hybrid": 0},
    "10-12": {"in_person": 77, "online": 66, "hybrid": 0},
    "13": {"in_person": 77, "online": 66, "hybrid": 0},
}

from enum import Enum


class course_type_schema(Enum):
    in_person = "in_person"
    online = "online"
    hybrid = "hybrid"


@router.get("/base_score/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def get_teacher_payment_score(course_id: sch.UUID, db=Depends(get_db)):
    course = dbf.get_course(db, course_id)
    course_cap, course_type = course.course_capacity, course.course_type
    match course_cap:
        case x if x <= 5:
            return Base_salary["1-5"][str(course_type.value)]
        case x if 6 <= x <= 9:
            return Base_salary["6-9"][str(course_type.value)]
        case x if 10 <= x <= 12:
            return Base_salary["10-12"][str(course_type.value)]
        case x if 13 <= x:
            return Base_salary["13"][str(course_type.value)]


@router.get("/base_field")
async def get_teacher_payment_field():
    return Base_salary.keys()


teacher_level = {
    "regular": 0,
    "expert": 22,
    "visiting / guest": 0,
    "exam / test": 30,
    "master": 40,
    "supervisor": 55,
    "master_Supervisor": 5.5,
    "director_of_education": 5.5
}


@router.get("/teacher_level/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def get_teacher_level(employee_id, db=Depends(get_db)):
    salary_policy = db.query(dbf.SalaryPolicy).filter_by(user_pk_id=employee_id, deleted=False).first()
    salary_policy = salary_policy.dict()
    teacher_level = salary_policy["teaching_level"]
    return teacher_level


@router.get("/course_cap")
async def get_course_cap():
    course_cap = {"1-5": 1, "6-9": 2, "10-12": 3, "13-50": 4}
    return course_cap


StudentAssignFeedback = {
    "weak": -5.5,
    "average": 0,
    "good": 5.5,
    "excellent": 11
}


@router.get("/student_assign_feedback")
async def get_student_assign_feedback():
    return StudentAssignFeedback


course_level = {
    "connect": 11,
    "FCE": 22,
    "CAE": 44,
    "CPE": 66
}


@router.get("/course_level")
async def get_course_level():
    return course_level


@router.get("/course_type")
async def get_course_type():
    course_type = {"Online": 0, "in_person": 11, "hybrid": 0}
    return course_type


survey_score = {
    "weak": 0,
    "average": 5.5,
    "excellent": 11
}


@router.get("/survey_score")
async def get_survey_score():
    return survey_score


LP_submission = {
    "0-50%_of_LP/weak": -11,
    "50-75%_of_LP/average": 5.5,
    "75-100%_of_LP/Good": 11,
    "100%_of_LP/Excellent": 16.5,
}


@router.get("/LP_submission")
async def get_LP_submission():
    return LP_submission


result_submission_to_FD = {
    "more_than_6_day": -5.5,
    "4_or_5_day": 0,
    "less_than_3_day": 5.5
}


@router.get("/result_submission_to_FD")
async def get_result_submission_to_FD():
    return result_submission_to_FD


course_cancellation = {
    "None": 11,
    "1": -5.5,
    "2": -7.5,
    "3": -16.5
}


@router.get("/course_cancellation")
async def get_course_cancellation():
    return course_cancellation


ReportToStudent = {
    "more_than_3_day/weak": -5.5,
    "2_day/average": 0,
    "1_day/good": 5.5,
    "no_delay/excellent": 11
}


@router.get("/ReportToStudent/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def ReportToStudent(course_id: sch.UUID, db=Depends(get_db)):
    status, result = dbf.get_course(db, course_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=result)

    course_cap = result.course_capacity
    return {k: v * course_cap for k, v in ReportToStudent.items()}


#  per semester
time_management = {
    "less_than_10_min": 11,
    "10_to_30_min": 5.5,
    "30_to_40_min": -5.5,
    "more_than_40_min": -16.5
}


@router.get("/time_management")
async def get_time_management():
    return time_management
