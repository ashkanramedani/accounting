import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Exist import employee_exist


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(
                teacher_tardy_reports_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_tardy_request(db: Session):
    try:
        data = db.query(dbm.Teacher_tardy_reports_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.create_by_fk_id, Form.teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"
        OBJ = dbm.Teacher_tardy_reports_form()

        OBJ.create_by_fk_id=Form.create_by_fk_id,
        OBJ.teacher_fk_id=Form.teacher_fk_id,
        OBJ.class_fk_id=Form.class_fk_id,
        OBJ.delay=Form.delay

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
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=form_id,
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


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(
                teacher_tardy_reports_pk_id=Form.teacher_tardy_reports_pk_id,
                deleted=False
        ).first()

        if not employee_exist(db, [Form.create_by_fk_id, Form.teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        if not record:
            return 404, "Not Found"
        record.create_by_fk_id = Form.create_by_fk_id
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
