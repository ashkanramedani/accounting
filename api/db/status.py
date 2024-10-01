from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def get_status(db: Session, status_id):
    try:
        return 200, db.query(dbm.Status_form).filter_by(status_pk_id=status_id).filter(dbm.Status_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_status(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Status_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_status(db: Session, Form: sch.post_status_schema):
    try:
        OBJ = dbm.Status_form(**Form.__dict__)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 201, OBJ

    except Exception as e:
        return Return_Exception(db, e)


def update_status(db: Session, Form: sch.update_status_schema):
    try:
        record = db.query(dbm.Status_form).filter_by(status_pk_id=Form.status_pk_id).filter(dbm.Status_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()

        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_status_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Status_form).filter_by(status_pk_id=form_id).first()
        if not record:
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)


def delete_status(db: Session, status_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).filter(dbm.Status_form.status != "deleted").first()
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)
