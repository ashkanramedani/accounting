import datetime
import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# business trip
def get_business_trip_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_business_trip_form(db: Session):
    try:
        return 200, db.query(dbm.Business_Trip_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_business_trip_form(db: Session, Form: sch.post_business_trip_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id]):
            return 400, "Bad Request"

        OBJ = dbm.Business_Trip_form()

        OBJ.employee_fk_id = Form.employee_fk_id
        OBJ.destination = Form.destination
        OBJ.description = Form.description

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_business_trip_form(db: Session, form_id):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(business_trip_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_business_trip_form(db: Session, Form: sch.update_business_trip_schema):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(
                business_trip_pk_id=Form.business_trip_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 400, "Bad Request"

        record.employee_fk_id = Form.employee_fk_id
        record.destination = Form.destination
        record.description = Form.description
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
