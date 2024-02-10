from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Exist import employee_exist


def get_payment_method(db: Session, payment_method_id):
    try:
        record = db.query(dbm.payment_method_form).filter_by(
                payment_method_pk_id=payment_method_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def get_all_payment_method(db: Session):
    try:
        data = db.query(dbm.payment_method_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def post_payment_method(db: Session, Form: sch.post_payment_method_schema):
    try:
        OBJ = dbm.payment_method_form()
        OBJ.employee_fk_id = Form.employee_fk_id
        OBJ.shaba = Form.shaba
        OBJ.card_number = Form.card_number

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "payment_method Added"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def delete_payment_method(db: Session, payment_method_id):
    try:
        record = db.query(dbm.payment_method_form).filter_by(
                payment_method_pk_id=payment_method_id,
                deleted=False
        ).first()
        if not record or record.deleted:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def update_payment_method(db: Session, Form: sch.update_payment_method_schema):
    try:
        record = db.query(dbm.payment_method_form).filter(dbm.payment_method_form.payment_method_pk_id == Form.payment_method_pk_id).first()
        if not record or record.deleted:
            return 404, "Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target employee Not Found"

        record.employee_fk_id = Form.employee_fk_id
        record.shaba = Form.shaba
        record.card_number = Form.card_number
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.args[0]
