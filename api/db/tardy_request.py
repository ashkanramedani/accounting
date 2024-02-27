import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=form_id,deleted=False).first()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_tardy_request(db: Session):
    try:
        return 200, db.query(dbm.Teacher_tardy_reports_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 400, "Bad Request"
        OBJ = dbm.Teacher_tardy_reports_form()

        print(f'{Form.created_fk_by}')
        OBJ.created_fk_by = Form.created_fk_by
        OBJ.teacher_fk_id = Form.teacher_fk_id
        OBJ.class_fk_id = Form.class_fk_id
        OBJ.delay = Form.delay

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=Form.teacher_tardy_reports_pk_id,deleted=False).first()

        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 400, "Bad Request"

        if not record:
            return 404, "Record Not Found"
        record.created_fk_by = Form.created_fk_by
        record.teacher_fk_id = Form.teacher_fk_id
        record.class_fk_id = Form.class_fk_id
        record.delay = Form.delay
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
