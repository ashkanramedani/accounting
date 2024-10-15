import datetime
from random import randint
from typing import List, Dict, Tuple

import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *

CAN_ACCEPT_ITEM = ["ready_to_use", "ready_to_pay"]


def get_shopping_card(db: Session, shopping_card_id: UUID):
    try:
        Shopping_card = db \
            .query(dbm.Shopping_card_form) \
            .filter_by(shopping_card_pk_id=shopping_card_id) \
            .filter(dbm.Shopping_card_form.status.in_(CAN_ACCEPT_ITEM)) \
            .first()
        return 200, Shopping_card
    except Exception as e:
        return Return_Exception(db, e)


def get_all_shopping_card(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Shopping_card_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)



def create_empty_shopping_card(db: Session, user_id: UUID):
    try:
        Shopping_card = db \
            .query(dbm.Shopping_card_form) \
            .filter_by(user_fk_id=user_id) \
            .filter(dbm.Shopping_card_form.status.in_(CAN_ACCEPT_ITEM)) \
            .first()
        if not Shopping_card:
            Shopping_card = dbm.Shopping_card_form(user_fk_id=user_id, status="ready_to_use")  # type: ignore
            db.add(Shopping_card)
            db.commit()
        return 200, Shopping_card


    except Exception as e:
        return Return_Exception(db, e)


def add_item(db: Session, shopping_card_id, Form: List[sch.add_to_card]):
    shopping_card = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).filter(dbm.Shopping_card_form.status != "deleted").first()
    if not shopping_card:
        return 400, "shopping_card Not Found"

    bucket: [dbm.Shopping_card_item_form] = []

    ItemIDs: List[UUID] = [item.item_id for item in Form]
    NOW = datetime.datetime.now(tz=IRAN_TIMEZONE)

    product_query: List[dbm.Products_Mapping_form] = db \
        .query(
            dbm.Products_Mapping_form) \
        .filter(
            dbm.Products_Mapping_form.products_mapping_pk_id.in_(ItemIDs)) \
        .all()

    reserve_product_id = sqlalchemy.orm.aliased(dbm.Shopping_card_item_form.product_fk_id)
    reserve_expire = sqlalchemy.orm.aliased(dbm.Shopping_card_item_form.expire_date)

    reserve_query: List[Tuple] = db \
        .query(
            reserve_product_id,
            func.sum(dbm.Shopping_card_item_form.quantity)) \
        .filter(
            reserve_product_id.in_(ItemIDs), reserve_expire > NOW) \
        .group_by(
            reserve_product_id) \
        .all()

    products: Dict[str, dbm.Products_Mapping_form] = {str(product.products_mapping_pk_id): product for product in product_query}
    reserves: Dict[str, int] = {str(product): product_count for product, product_count in reserve_query}

    WARN = []
    for item in Form:
        if item.item_id not in products:
            WARN.append(f'Product with not found. ID: {item.item_id}')
        elif products[str(item.item_id)].product_quantity - reserves.get(str(item.item_id), 0) < item.quantity:
            WARN.append(f"Not Enough item {item.item_id}")
        else:
            existing: dbm.Shopping_card_item_form = db.query(dbm.Shopping_card_item_form).filter_by(shopping_card_fk_id=shopping_card_id, product_fk_id=item.item_id).first()
            if existing:
                existing.quantity += item.quantity
                db.flush()
            else:
                bucket.append(dbm.Shopping_card_item_form(shopping_card_fk_id=shopping_card_id, product_fk_id=item.item_id, quantity=item.quantity, expire_date=NOW + datetime.timedelta(hours=1)))  # type: ignore

    db.add_all(bucket)
    db.commit()
    return 200, f'Items has been Added. {(WARN if WARN else "")}'


def delete_shopping_card(db: Session, shopping_card_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Shopping_card_form).filter_by(shopping_card_pk_id=shopping_card_id).filter(dbm.Shopping_card_form.status != "deleted").first()
        if not record:
            return 400, "shopping_card Not Found"

        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
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
