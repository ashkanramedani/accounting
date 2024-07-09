from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import db as dbf
import schemas as sch
from db.models import get_db

router = APIRouter(prefix='/api/v1/form/course', tags=['Course'])


# tardy request
@router.post("/add", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], status_code=201, response_model=sch.Base_record_add)
async def add_course(Form: sch.post_course_schema, db=Depends(get_db)):
    status_code, result = dbf.post_course(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.course_response)
async def search_course(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_course(db, form_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.course_response])
async def search_all_course(course_type: str = None, db=Depends(get_db), page: sch.NonNegativeInt = 1, limit: sch.PositiveInt = 10, order: sch.Sort_Order = "desc"):
    status_code, result = dbf.get_all_course(db, course_type, page, limit, order)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/delete/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def delete_course(course_id, db=Depends(get_db)):
    status_code, result = dbf.delete_course(db, course_id)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/update", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
async def update_course(Form: sch.update_course_schema, db=Depends(get_db)):
    status_code, result = dbf.update_course(db, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result

# @router.put("/Report/{course_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
# async def update_course(course_id, Form: sch.teacher_salary_report, db=Depends(get_db)):
#     status_code, result = dbf.teacher_salary_report(db, course_id)
#     if status_code not in sch.SUCCESS_STATUS:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result

# def Course_Get_All(Course_client: TestClient):
#     res = Course_client.get("/search")
#     return Route_Result(route="/search", status=res.status_code, body=res.json)
#
# def Course():
#     logger.info("[DEV] Course Started")
#     Result_Obj = Result()
#     Course_client = TestClient(course_route)
#     Result_Obj.result.append(Course_Get_All(Course_client))
#     return Result
#
#
# @router.get("/search/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])  # , response_model=sch.course_response)
# async def search_course(form_id, db=Depends(get_db)):
#     status_code, result = dbf.get_course(db, form_id)
#     if status_code not in sch.SUCCESS_STATUS:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result
