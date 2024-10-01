import datetime
from typing import List, Literal

from .Base import *


@router.post("/employee", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Return_Salary])
async def employee_salary(Form: sch.Input, db=Depends(get_db)):
    status_code, result = dbf.employee_salary(db, Form.year, Form.month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/employee/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
async def search_report(employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
    if month > 12:
        raise HTTPException(status_code=400, detail="Invalid Month")
    status_code, result = dbf.employee_salary_report(db, employee_id, year, month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/employee/search", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
async def search_employee_salary(employee_id: UUID, target_date: datetime.date, field: Literal["create", "update"] = "create", db=Depends(get_db)):
    status_code, result = dbf.get_employee_salary(db, employee_id, target_date, field)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result

#
# @router.get("/sand/", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
# async def sand_search_report(db=Depends(get_db)):
#     employee_id = "00000001-0000-4b94-8e27-44833c2b940f"
#     year = 2025
#     month = 1
#     status_code, result = dbf.employee_salary_report(db, employee_id, year, month)
#     if status_code not in sch.SUCCESS_STATUS:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result


@router.put("/employee/update/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
async def update_teacher_report(form_id: UUID, Form: sch.update_salary_report, db=Depends(get_db)):
    status_code, result = dbf.update_employee_salary(db, form_id, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
