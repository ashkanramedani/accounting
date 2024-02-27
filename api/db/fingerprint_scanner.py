import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


# Teacher Replacement
def get_fingerprint_scanner(db: Session, user_id):
    try:
        user = db.query(dbm.Employees_form).filter_by(employees_pk_id=user_id, deleted=False).first()
        if not user:
            return 400, "Bad Request"
        return 200, db.query(dbm.fingerprint_scanner_form).filter_by(user_ID=user.fingerprint_scanner_user_id, deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_fingerprint_scanner(db: Session):
    try:
        return 200, db.query(dbm.fingerprint_scanner_form).filter_by(deleted=False).all()
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        OBJ = dbm.fingerprint_scanner_form()

        OBJ.created_fk_by = Form.created_fk_by
        OBJ.In_Out = Form.In_Out
        OBJ.Antipass = Form.Antipass
        OBJ.ProxyWork = Form.ProxyWork
        OBJ.DateTime = Form.DateTime
        OBJ.user_ID = Form.user_ID

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_bulk_fingerprint_scanner(db: Session, Form: sch.post_bulk_fingerprint_scanner_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        result = {}

        for record in Form.Records:
            try:
                OBJ = dbm.fingerprint_scanner_form()

                OBJ.created_fk_by = Form.created_fk_by
                OBJ.user_ID = record.user_ID
                OBJ.In_Out = record.In_Out
                OBJ.Antipass = record.Antipass
                OBJ.ProxyWork = record.ProxyWork
                OBJ.DateTime = datetime.strptime(record.DateTime, "%Y-%m-%d %H:%M:%S")

                db.add(OBJ)
                db.commit()
                db.refresh(OBJ)
            except Exception as e:
                db.rollback()
                return 500, e.__repr__()
        return 200, result
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.fingerprint_scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.fingerprint_scanner_form).filter_by(teacher_tardy_reports_pk_id=Form.fingerprint_scanner_pk_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.employee_fk_id]):
            return 400, "Bad Request"

        record.employee_fk_id = Form.employee_fk_id
        record.created_fk_by = Form.created_fk_by
        record.In_Out = Form.In_Out
        record.Antipass = Form.Antipass
        record.ProxyWork = Form.ProxyWork
        record.DateTime = Form.DateTime
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
