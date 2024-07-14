from sqlalchemy.orm import Session

import schemas as sch
from db import models as dbm
from db.Extra import *


def get_payment_method(db: Session, payment_method_id):
    try:
        return 200, db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id).filter(dbm.Payment_Method_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_payment_method(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        # Records = record_order_by(db,dbm.Payment_Method_form, page, limit, order, SortKey)
        # New = []
        #
        # for record in Records:
        #
        #     record.shaba = "Edited"
        #     record.card_number = "Edited"
        #     logger.warning(record.__dict__)
        #     New.append(record)
        return record_order_by(db,dbm.Payment_Method_form, page, limit, order, SortKey)
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
        record = db.query(dbm.Payment_Method_form).filter_by(payment_method_pk_id=payment_method_id).filter(dbm.Payment_Method_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
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
