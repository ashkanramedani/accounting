from datetime import datetime
import sqlalchemy.sql.expression as sse
import api.schemas as sch
from sqlalchemy import desc, asc
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from typing import Optional, List, Dict, Any

from api.lib import unique
import logging
import models as dbm
from sqlalchemy.orm import Session


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


# Leave Forms
def get_leave_form(db: Session, form_id: int):
    try:
        data = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == form_id).first()
        if data:
            return data
        return f"employee leave form Not Fount with ID: {form_id}"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def post_leave_form(db: Session, Form: sch.Leave_request_schema):
    try:
        OBJ = dbm.Leave_request_form(
                employee_id=Form.employee_id,
                start_date=Form.start_date,
                end_date=Form.end_date,
                Description=Form.Description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 1
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def delete_leave_form(db: Session, leave_form_id: int):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == leave_form_id).delete()
        # if record.deleted is True:
        db.commit()

    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1


def update_leave_form(db: Session, Form: sch.Leave_request_schema, leave_request_id: int):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == leave_request_id).first()
        record.employee_id = Form.employee_id
        record.Start_Date = Form.start_date,
        record.End_Date = Form.end_date,
        record.Description = Form.Description
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1