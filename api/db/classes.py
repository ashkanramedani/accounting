from lib import log
logger = log()
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


def get_class(db: Session, class_id):
    try:
        return 200, db.query(dbm.Class_form).filter_by(class_pk_id=class_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_class(db: Session):
    try:
        return 200, db.query(dbm.Class_form).filter_by(deleted=False).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_class(db: Session, Form: sch.post_class_schema):
    try:
        OBJ = dbm.Class_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "class Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_class(db: Session, class_id):
    try:
        record = db.query(dbm.Class_form).filter_by(class_id=class_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_class(db: Session, Form: sch.update_class_schema):
    try:
        record = db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_pk_id,deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
