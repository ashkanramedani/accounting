from typing import Tuple, List, Dict

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from db.Extra import *
from lib import logger, Separate_days


def get_business_trip_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id).filter(dbm.Business_Trip_form.status != "deleted").first()
    except Exception as e:
        logger.error(e)
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_business_trip_form(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db,dbm.Business_Trip_form, page, limit, order, SortKey)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_business_trip(db: Session, user_fk_id, start_date, end_date):
    try:
        Business_Trip_report = db.query(dbm.Business_Trip_form) \
            .filter_by(user_fk_id=user_fk_id) \
            .filter(dbm.Business_Trip_form.date.between(start_date, end_date)) \
            .filter(dbm.Business_Trip_form.status != "deleted") \
            .all()
        return 200, Business_Trip_report
    except Exception as e:
        return Return_Exception(db, e)


def post_business_trip_form(db: Session, Form: sch.post_business_trip_schema) -> Tuple[int, str | Dict | List]:
    try:
        # db.query(dbm.Business_Trip_form).filter_by(star)
        if not employee_exist(db, [Form.user_fk_id, Form.user_fk_id]):
            return 400, "Bad Request: Employee not found"

        data = Form.dict()

        Start, End = Fix_datetime(data.pop("start_date")), Fix_datetime(data.pop("end_date"))

        if End < Start:
            return 400, "Bad Request: End Date must be greater than Start Date"

        OBJs = []
        for Day in Separate_days(Start, End):
            OBJs.append(dbm.Business_Trip_form(**Day, **data))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_business_trip_form(db: Session, form_id):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id).filter(dbm.Business_Trip_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_business_trip_form(db: Session, Form: sch.update_business_trip_schema):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=Form.business_trip_pk_id).filter(dbm.Business_Trip_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def Verify_business_trip(db: Session, Form: sch.Verify_business_trip_schema):
    try:
        Warn = []
        verified = 0
        records = db.query(dbm.Business_Trip_form) \
            .filter(dbm.Business_Trip_form.status == "submitted") \
            .filter(dbm.Business_Trip_form.business_trip_pk_id.in_(Form.business_trip_id)) \
            .all()

        for record in records:
            record.status = Set_Status(db, "form", "verified")
            verified += 1

        db.commit()
        if Warn:
            return 200, f"{verified} Form Verified. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Verified."
    except Exception as e:
        return Return_Exception(db, e)
