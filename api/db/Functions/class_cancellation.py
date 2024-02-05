import logging
from uuid import UUID
from .Exist import employee_exist
from sqlalchemy.orm import Session
from typing import List
import schemas as sch
import db.models as dbm
from .Exist import employee_exist


# class_cancellation
def get_class_cancellation_form(db: Session, form_id):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_class_cancellation_form(db: Session):
    try:
        data = db.query(dbm.Class_Cancellation_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_class_cancellation_form(db: Session, Form: sch.post_class_cancellation_schema):
    try:
        if not employee_exist(db, [Form.teacher_fk_id, Form.create_by_fk_id]):
            return 404, "Target Employee Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        OBJ = dbm.Class_Cancellation_form(
                create_by_fk_id=Form.create_by_fk_id,
                class_fk_id=Form.class_fk_id,
                teacher_fk_id=Form.teacher_fk_id,
                replacement=Form.replacement,
                class_duration=Form.class_duration,
                class_location=Form.class_location,
                description=Form.description,
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_class_cancellation_form(db: Session, form_id):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_class_cancellation_form(db: Session, Form: sch.update_class_cancellation_schema):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=Form.class_cancellation_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.teacher_fk_id, Form.create_by_fk_id]):
            return 404, "Target Employee Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        record.create_by_fk_id = Form.create_by_fk_id
        record.class_fk_id = Form.class_fk_id
        record.teacher_fk_id = Form.teacher_fk_id
        record.replacement = Form.replacement
        record.class_duration = Form.class_duration
        record.class_location = Form.class_location
        record.description = Form.description

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()

