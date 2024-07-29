from sqlalchemy.orm import Session

import schemas as sch
from db import models as dbm
from db.Extra import *


# Sub Request
def get_session_cancellation(db: Session, form_id):
    try:
        return 200, db.query(dbm.Session_Cancellation_form).filter_by(session_cancellation_pk_id=form_id).filter(dbm.Session_Cancellation_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_session_cancellation(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Session_Cancellation_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_session_cancellation(db: Session, Form: sch.post_Session_Cancellation_schema):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_fk_id).filter(dbm.Session_form.status != "deleted").first()
        if not session:
            return 400, "Session not found"
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: Employee Not Found"

        session.status = Set_Status(db, "form", "canceled")
        session.canceled = True
        OBJ = dbm.Session_Cancellation_form(**Form.__dict__, status=Set_Status(db, "form", "approved"))  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_session_cancellation(db: Session, form_id):
    try:
        record = db.query(dbm.Session_Cancellation_form).filter_by(session_cancellation_pk_id=form_id).filter(dbm.Session_Cancellation_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_session_cancellation():
    return 400, f'Session Cancellation forms cant be Updated.'
