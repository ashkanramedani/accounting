from .Base import *

# Form: sch.teacher_salary_report

@router.get("/teacher/courses", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Teacher_course_report])
async def teacher_course(db=Depends(get_db)):
    status_code, result = dbf.teacher_courses(db)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/teacher/sub_courses/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Teacher_subcourse_report])
async def teacher_sub_course(course_id: UUID, db=Depends(get_db)):
    status_code, result = dbf.teacher_sub_courses(db, course_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
