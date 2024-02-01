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


# Leave Request
def get_leave_request(db: Session, Form: sch.get_leave_request_schema):
    try:
        if isinstance(Form.form_id, int):
            data = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == Form.form_id).first()
        else:
            data = db.query(dbm.Leave_request_form).first()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        OBJ = dbm.Leave_request_form(
                created_by_fk_id=Form.created_by,
                created_for_fk_id=Form.created_for,
                start_date=Form.start_date,
                end_date=Form.end_date,
                Description=Form.Description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_leave_request(db: Session, Form: sch.delete_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == Form.form_id).delete()
        if not record or record.deleted is True:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter(dbm.Leave_request_form.leave_request_pk_id == Form.leave_request_id).first()
        if not record:
            return 404, "Not Found"
        record.created_by_fk_id = Form.created_by
        record.created_for_fk_id = Form.created_for
        record.Start_Date = Form.start_date,
        record.End_Date = Form.end_date,
        record.Description = Form.Description
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()

