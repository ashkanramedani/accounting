from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def get_product_mapping(db: Session, product_mapping_id):
    try:
        return 200, db.query(dbm.Products_Mapping_form).filter_by(product_pk_id=product_mapping_id).filter(dbm.Products_Mapping_form.product_mapping != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_product_mapping(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Products_Mapping_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_product_mapping(db: Session, Form: sch.post_product_mapping_schema):
    try:
        OBJ = dbm.Products_Mapping_form(**Form.__dict__)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 201, OBJ

    except Exception as e:
        return Return_Exception(db, e)


def update_product_mapping(db: Session, Form: sch.update_product_mapping_schema):
    try:
        record = db.query(dbm.Products_Mapping_form).filter_by(product_pk_id=Form.products_mapping_pk_id).filter(dbm.Products_Mapping_form.product_mapping != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()

        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_product_mapping_status(db: Session, form_id: UUID, product_mapping_id: UUID):
    try:
        record = db.query(dbm.Products_Mapping_form).filter_by(product_pk_id=form_id).first()
        if not record:
            return 400, "Record Not Found"

        product_mapping = db.query(dbm.Products_Mapping_form).filter_by(product_pk_id=product_mapping_id).first()
        if not product_mapping:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(product_mapping=record.product_mapping, table_name=record.__tablename__))
        record.product_mapping = product_mapping.product_mapping_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)


def delete_product_mapping(db: Session, product_mapping_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Products_Mapping_form).filter_by(product_pk_id=product_mapping_id).filter(dbm.Products_Mapping_form.product_mapping != "deleted").first()
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)
