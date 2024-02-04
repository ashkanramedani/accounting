from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

import schemas as sch
from db.database import get_db
import db as dbf

router = APIRouter(prefix='/api/v1/form', tags=['Form'])


# leave forms
@router.post("/leave_request/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_leave_request(Form: sch.post_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_leave_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/leave_request/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_leave_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_leave_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/leave_request/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_leave_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/leave_request/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_leave_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_leave_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/leave_request/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_leave_request(Form: sch.update_leave_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_leave_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# tardy request
@router.post("/tardy_request/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_tardy_request(Form: sch.post_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.post_tardy_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tardy_request/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/tardy_request/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_tardy_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_leave_request(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/tardy_request/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_tardy_request(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/tardy_request/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_tardy_request(Form: sch.update_teacher_tardy_reports_schema, db=Depends(get_db)):
    status_code, result = dbf.update_tardy_request(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# Teacher replacement

@router.post("/teacher_replacement/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_teacher_replacement(Form: sch.post_teacher_replacement_schema, db=Depends(get_db)):
    status_code, result = dbf.post_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/teacher_replacement/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_teacher_replacement(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/teacher_replacement/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_teacher_replacement(db=Depends(get_db)):
    status_code, result = dbf.get_all_teacher_replacement(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/teacher_replacement/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_tardy_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_teacher_replacement(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/teacher_replacement/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_tardy_request(Form: sch.update_teacher_replacement_schema, db=Depends(get_db)):
    status_code, result = dbf.update_teacher_replacement(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# business trip
@router.post("/business_trip/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_business_trip(Form: sch.post_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.post_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/business_trip/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/business_trip/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_business_trip(db=Depends(get_db)):
    status_code, result = dbf.get_all_business_trip_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/business_trip/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/business_trip/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_business_trip(Form: sch.update_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.update_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# business trip
@router.post("/business_trip/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_business_trip(Form: sch.post_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.post_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/business_trip/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/business_trip/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_business_trip(db=Depends(get_db)):
    status_code, result = dbf.get_all_business_trip_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/business_trip/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_business_trip(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_business_trip_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/business_trip/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_business_trip(Form: sch.update_business_trip_schema, db=Depends(get_db)):
    status_code, result = dbf.update_business_trip_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# Class cancellation
@router.post("/class_cancellation/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_class_cancellation(Form: sch.post_class_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.post_class_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/class_cancellation/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_class_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_class_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/class_cancellation/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_class_cancellation(db=Depends(get_db)):
    status_code, result = dbf.get_all_class_cancellation_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/class_cancellation/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_class_cancellation(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_class_cancellation_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/class_cancellation/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_class_cancellation(Form: sch.update_class_cancellation_schema, db=Depends(get_db)):
    status_code, result = dbf.update_class_cancellation_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


# remote_request
@router.post("/remote_request/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_remote_request(Form: sch.post_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/remote_request/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/remote_request/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_remote_request_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/remote_request/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/remote_request/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_remote_request(Form: sch.update_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

# Question
@router.post("/remote_request/add", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def add_remote_request(Form: sch.post_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.post_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/remote_request/search/{form_id}", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.get_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.get("/remote_request/search", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def search_remote_request(db=Depends(get_db)):
    status_code, result = dbf.get_all_remote_request_form(db)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.delete("/remote_request/delete", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def delete_remote_request(form_id, db=Depends(get_db)):
    status_code, result = dbf.delete_remote_request_form(db, form_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


@router.put("/remote_request/update", dependencies=[Depends(RateLimiter(times=10, seconds=5))])
async def update_remote_request(Form: sch.update_remote_request_schema, db=Depends(get_db)):
    status_code, result = dbf.update_remote_request_form(db, Form)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

