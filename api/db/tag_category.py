from typing import List
from uuid import UUID

from lib import logger


from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *

def get_tag(db: Session, tag_id):
    try:
        return 200, db.query(dbm.Tag_form).filter_by(tag_pk_id=tag_id, deleted=False).first()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_tag(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Tag_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_tag(db: Session, Form: sch.post_tag_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Employee Not Found"
        OBJ = dbm.Tag_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_tag(db: Session, tag_id):
    try:
        record = db.query(dbm.Tag_form).filter_by(tag_pk_id=tag_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_tag(db: Session, Form: sch.update_tag_schema):
    try:
        record = db.query(dbm.Tag_form).filter_by(tag_pk_id=Form.tag_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_category(db: Session, category_id):
    try:
        return 200, db.query(dbm.Category_form).filter_by(category_pk_id=category_id, deleted=False).first()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_category(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Category_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_category(db: Session, Form: sch.post_category_schema):
    try:
        OBJ = dbm.category_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, f'category Added. ID: {OBJ.category_pk_id}'
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_category(db: Session, category_id):
    try:
        record = db.query(dbm.Category_form).filter_by(category_pk_id=category_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_category(db: Session, Form: sch.update_category_schema):
    try:
        record = db.query(dbm.Category_form).filter_by(category_pk_id=Form.category_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
