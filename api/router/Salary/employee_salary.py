from .Base import *


@router.post("/employee", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=List[sch.Return_Salary])
async def employee_salary(Form: sch.Input, db=Depends(get_db)):
    status_code, result = dbf.employee_salary(db, Form.year, Form.month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/employee/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
async def search_report(employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
    if not employee_id:
        raise HTTPException(status_code=400, detail="Employee ID Not provided")
    if not year:
        raise HTTPException(status_code=400, detail="Year Not provided")
    if not month:
        raise HTTPException(status_code=400, detail="Month Not provided")
    if month > 12:
        raise HTTPException(status_code=400, detail="Invalid Month")
    status_code, result = dbf.employee_salary_report(db, employee_id, year, month)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result


#
# @router.post("/search/{employee_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))])
# async def search_teacher_report(employee_id: UUID, year: sch.PositiveInt, month: sch.PositiveInt, db=Depends(get_db)):
#     raise HTTPException(status_code=501, detail="Not Implemented")
#     status_code, result = dbf.get_employee_salary(db, employee_id, year, month)
#     if status_code not in sch.SUCCESS_STATUS:
#         raise HTTPException(status_code=status_code, detail=result)
#     return result


@router.put("/employee/update/{form_id}", dependencies=[Depends(RateLimiter(times=1000, seconds=1))], response_model=sch.employee_salary_Response)
async def update_teacher_report(form_id: UUID, Form: sch.update_employee_salary, db=Depends(get_db)):
    status_code, result = dbf.update_employee_salary(db, form_id, Form)
    if status_code not in sch.SUCCESS_STATUS:
        raise HTTPException(status_code=status_code, detail=result)
    return result
