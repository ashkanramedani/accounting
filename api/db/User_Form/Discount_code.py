import datetime
from random import choices
from string import ascii_letters, digits

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def generate_unique_discount_code(existing_codes):
    while True:
        new_code = ''.join(choices(ascii_letters + digits, k=8))
        if new_code not in existing_codes:
            return new_code


def get_discount_code(db: Session, discount_code_id):
    try:
        return 200, db.query(dbm.Discount_code_form).filter_by(discount_code_pk_id=discount_code_id).filter(dbm.Discount_code_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_discount_code(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Discount_code_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_discount_code(db: Session, Form: sch.post_discount_code_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"
        Existing_Code = (db.query(dbm.Discount_code_form.discount_code).all())
        OBJ = dbm.Discount_code_form(**Form.dict(), discount_code=generate_unique_discount_code(Existing_Code))  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "discount_code Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_discount_code(db: Session, discount_code_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Discount_code_form).filter_by(discount_code_pk_id=discount_code_id).filter(dbm.Discount_code_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_discount_code(db: Session, Form: sch.update_discount_code_schema):
    try:
        record = db.query(dbm.Discount_code_form).filter_by(discount_code_pk_id=Form.discount_code_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_discount_code_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Discount_code_form).filter_by(discount_code_pk_id=form_id).first()
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


def apply_discount_code(db: Session, Form: sch.apply_code):
    """
        return new price if discount_code is valid
    """
    try:
        record = db \
            .query(dbm.Discount_code_form) \
            .filter_by(discount_code=Form.discount_code) \
            .filter(dbm.Discount_code_form.status != "deleted") \
            .first()

        if not record:
            return 400, "Discount Code Not Found"

        now = datetime.datetime.now(tz=IRAN_TIMEZONE)
        if record.start_date and now < record.start_date:
            return 400, "Discount Code not available yet"
        if record.end_date and record.end_date < now:
            return 400, "Discount Code Expired"

        if record.target_user and record.target_user != Form.target_user:
            return 400, "target user cant use this code"

        if record.target_product and record.target_product != Form.target_product:
            return 400, "target product cant use this code"

        match record.discount_type:
            case "percentage":
                discounted_price = Form.price - (Form.price * record.discount_amount / 100)
            case "fix":
                discounted_price = Form.price - record.discount_amount
            case _:
                return 400, "Invalid Discount Type"

        return 200, round(max(discounted_price, 0), 2)

    except Exception as e:
        return Return_Exception(db, e)
