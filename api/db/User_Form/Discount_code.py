from random import choices

from sqlalchemy.orm import Session

from string import ascii_letters, digits

import schemas as sch
import models as dbm
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
