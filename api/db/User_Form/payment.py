from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def get_payment_method(db: Session, payment_method_id, user: bool = False):
    try:
        if user:
            return 200, db.query(dbm.Payment_Method_form).filter_by(user_fk_id=payment_method_id).filter(dbm.Payment_Method_form.status != "deleted").all()
        return 200, db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id).filter(dbm.Payment_Method_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_payment_method(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Payment_Method_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_payment_method(db: Session, Form: sch.post_payment_method_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.user_fk_id]):
            return 400, "Bad Request"

        OBJ = dbm.Payment_Method_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "payment_method Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_payment_method(db: Session, payment_method_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id).filter(dbm.Payment_Method_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_payment_method(db: Session, Form: sch.update_payment_method_schema):
    try:
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=Form.payment_method_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_payment_method_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=form_id).first()
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
