from typing import Tuple, List, Dict

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger

from ..Extra import *

from lib.Date_Time import Fix_datetime

def get_business_trip_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_business_trip_form(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Business_Trip_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_business_trip(db: Session, salary_rate, employee_fk_id, start_date, end_date) -> Tuple[int, dict | str]:
    if not salary_rate.business_trip_permission:
        return 200, {"business_trip": 0, "business_trip_earning": 0}
    Business_Trip_report = (
        db.query(dbm.Business_Trip_form)
        .filter_by(deleted=False, employee_fk_id=employee_fk_id)
        .filter(dbm.Business_Trip_form.end_date.between(start_date, end_date))
        .all()
    )

    total_business = sum(row.duration for row in Business_Trip_report)
    business_trip = min(total_business, salary_rate.business_trip_cap)
    return 200, {"business_trip": business_trip, "business_trip_earning": business_trip * salary_rate.business_trip_factor}


def post_business_trip_form(db: Session, Form: sch.post_business_trip_schema) -> Tuple[int, str | Dict | List]:
    try:
        # db.query(dbm.Business_Trip_form).filter_by(star)
        if not employee_exist(db, [Form.employee_fk_id]):
            return 400, "Bad Request: Employee not found"

        data = Form.dict()
        Start, End = Fix_datetime(data["start_date"]), Fix_datetime(data["end_date"])

        if End < Start:
            return 400, "Bad Request: End Date must be greater than Start Date"

        data = Form.dict()
        OBJ = dbm.Business_Trip_form(duration=(End - Start).total_seconds() // 60, **data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_business_trip_form(db: Session, form_id):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_business_trip_form(db: Session, Form: sch.update_business_trip_schema):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(
                business_trip_pk_id=Form.business_trip_pk_id,
                deleted=False
        )
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
