import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Exist import employee_exist


# Teacher Replacement
def get_fingerprint_scanner(db: Session, user_id):
    try:

        user = db.query(dbm.Employees_form).filter_by(
                employees_pk_id=user_id,
                deleted=False
        ).first()
        if not user:
            return 404, "User Not Found"

        record = db.query(dbm.fingerprint_scanner_form).filter_by(
                user_ID=user.fingerprint_scanner_user_id,
                deleted=False
        ).all()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.args[0]


def get_all_fingerprint_scanner(db: Session):
    try:
        data = db.query(dbm.fingerprint_scanner_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.args[0]


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_by_fk_id]):
            return 404, "Target Employee Not Found"

        OBJ = dbm.fingerprint_scanner_form()

        OBJ.created_by_fk_id = Form.created_by_fk_id
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
        return 500, e.args[0]


def post_bulk_fingerprint_scanner(db: Session, Form: sch.post_bulk_fingerprint_scanner_schema):
    try:

        if not employee_exist(db, [Form.created_by_fk_id]):
            return 404, "Target Employee Not Found"

        result = {}

        for User_ID, details in Form:
            for _, detail in details:
                try:
                    OBJ = dbm.fingerprint_scanner_form()
                    OBJ.created_by_fk_id = Form.created_by_fk_id
                    OBJ.user_ID = User_ID
                    OBJ.In_Out = detail['In_Out']
                    OBJ.Antipass = detail['Antipass']
                    OBJ.ProxyWork = detail['ProxyWork']
                    OBJ.DateTime = detail['DateTime']
                    db.add(OBJ)
                    db.commit()
                    db.refresh(OBJ)
                    result[User_ID] = "User Added"
                except Exception as e:
                    result[User_ID] = e.args[0]
                    db.rollback()
        return 200, result
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.args[0]


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.fingerprint_scanner_form).filter_by(
                fingerprint_scanner_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.fingerprint_scanner_form).filter_by(
                teacher_tardy_reports_pk_id=Form.fingerprint_scanner_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.created_by_fk_id, Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        record.employee_fk_id = Form.employee_fk_id
        record.created_by_fk_id = Form.created_by_fk_id
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
        return 500, e.args[0]
