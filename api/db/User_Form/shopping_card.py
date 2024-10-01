from typing import List, Dict

from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


# shopping_card

def get_shopping_card(db: Session, shopping_card_id):
    try:
        return 200, db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).filter(dbm.Shopping_card_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_shopping_card(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Shopping_card_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_shopping_card(db: Session, Form: sch.post_shopping_card_schema):
    try:
        data = Form.__dict__
        discount_code = data.pop("discount_code", None)
        bucket: List[sch.shopping_card_Item] = data.pop("bucket", [])

        total = 0.0
        for item in bucket:
            total += item.quantity * item.price

        total_discounted = total
        if discount_code:
            if not (discount := db.query(dbm.Discount_code_form).filter_by(discount_code=discount_code).filter(dbm.Discount_code_form.status != "deleted").first()):
                return 400, "Not a valid discount code"

            match discount.discount_type:
                case "percentage":
                    total_discounted = max(total - discount.discount_amount, 0)
                case "fix":
                    total_discounted = (total / 100) * discount.discount_amount

        OBJ = dbm.Shopping_card_form(**data, total=total, total_discounted=total_discounted)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_shopping_card(db: Session, shopping_card_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).filter(dbm.Shopping_card_form.status != "deleted").first()
        if not record:
            return 400, "shopping_card Record Not Found"

        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_shopping_card(db: Session, Form: sch.update_shopping_card_schema):
    try:
        record = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=Form.shopping_card_pk_id).filter(dbm.Shopping_card_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_shopping_card_status(db: Session, shopping_card_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).first()
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


def refresh_shopping_card(db: Session, shopping_card_id: UUID):
    try:
        record: dbm.Shopping_card_form = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).first()
        if not record:
            return 400, "Record Not Found"

        bucket: List[Dict] = record.bucket
        items_id = {item["item_pk_id"]: {**item} for item in bucket}

        product: List[dbm.Products_Mapping_form] = db.query(dbm.Products_Mapping_form).filter(dbm.Products_Mapping_form.products_mapping_pk_id.in_(items_id.keys())).all()

        WARN = {}
        for item in product:
            if (item_needed := items_id[item.products_mapping_pk_id]["quantity"]) > item.quantity:
                WARN[item.product_name] = {"item_needed": item_needed, "item_available": item.quantity, "WARN": "Not Enough Stock"}
            if (item_price := items_id[item.products_mapping_pk_id]["price"]) != item.product_price:
                WARN[item.product_name] = {"item_price": item_price, "new_price": item.product_price, "WARN": "Price Change"}
        if WARN:
            return 400, WARN
        return 200, record
    except Exception as e:
        return Return_Exception(db, e)
