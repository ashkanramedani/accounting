from lib import logger
from sqlalchemy.orm import Session
import db.models as dbm
import schemas as sch
from .Extra import *


def get_payment_method(db: Session, payment_method_id):
    try:
        return 200, db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_payment_method(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Payment_Method_form, page, limit, order)
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


def delete_payment_method(db: Session, payment_method_id):
    try:
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_payment_method(db: Session, Form: sch.update_payment_method_schema):
    try:
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=Form.payment_method_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.user_fk_id]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
