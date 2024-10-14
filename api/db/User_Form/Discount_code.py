import datetime
from typing import Literal, List, Dict
from random import choices
from string import ascii_letters, digits

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *

def apply_code_on_price(price: float, record: dbm.Discount_code_form):
    discount_type , discount_amount = record.discount_type, record.discount_amount
    if discount_type == "percentage":
        discounted_price = price - (price * discount_amount / 100)
    else:
        discounted_price = price - discount_amount
    return 200, round(max(discounted_price, 0), 2)

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
        from lib import logger
        logger.error(e)
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

        shopping_card = db \
            .query(dbm.Shopping_card_form) \
            .filter_by(shopping_card_fk_id=Form.shopping_card_id) \
            .first()

        if not shopping_card:
            return 400, "shopping card not found"

        now = datetime.datetime.now(tz=IRAN_TIMEZONE)

        if record.start_date and now < record.start_date or record.end_date and record.end_date < now:
            return 400, "Discount Code not available at this time"

        if record.target_user and record.target_user != shopping_card.user_fk_id:
            return 400, "target user cant use this code"


        elif record.target_product:
            Bucket: List[dbm.Shopping_card_item_form] = db.query(dbm.Shopping_card_item_form).filter_by(shopping_card_fk_id=Form.shopping_card_id).all()
            product_in_card: dbm.Shopping_card_item_form = next((key for key in Bucket if key.product_fk_id == record.target_product), None)
            TOTAL = 0
            TOTAL_Discounted = 0
            for product in Bucket:
                product_in_mapping = db.query(dbm.Products_Mapping_form).filter_by(products_mapping_pk_id=product_in_card.product_fk_id).first()
                product_in_card.pri = apply_code_on_price(product_in_mapping.discounted_price, record)
                Bucket: List[sch.shopping_card_Item] = [item for item in Unpacked_bucket.values()]
                shopping_card.bucket = Bucket
                db.commit()
                return 200, shopping_card

        else:
            shopping_card.total_discounted = apply_code_on_price(shopping_card.total_discounted, record)
            db.commit()
            return 200, shopping_card

    except Exception as e:
        return Return_Exception(db, e)


"""
class Shopping_card_item_form(Base):
    __tablename__ = "shopping_card_item"

    shopping_card_item_pk_id = create_Unique_ID()
    shopping_card_fk_id = create_foreignKey("Shopping_card_form")
    product_fk_id = create_foreignKey("Products_Mapping_form")

    quantity = Column(Integer, nullable=False, default=1)
    expire_date = Column(DateTime, default=None)
"""
