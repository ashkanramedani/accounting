import logging

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Exist import employee_exist
from .employee import get_all_employee


# Teacher Replacement
def get_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.fingerprint_scanner_form).filter_by(
                fingerprint_scanner_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_fingerprint_scanner(db: Session):
    try:
        data = db.query(dbm.fingerprint_scanner_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_by_fk_id, Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        OBJ = dbm.fingerprint_scanner_form()

        OBJ.employee_fk_id = Form.employee_fk_id
        OBJ.created_by_fk_id = Form.created_by_fk_id
        OBJ.In_Out = Form.In_Out
        OBJ.Antipass = Form.Antipass
        OBJ.ProxyWork = Form.ProxyWork
        OBJ.DateTime = Form.DateTime

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

        status_code, all_employee = get_all_employee(db)
        if status_code != 200:
            return status_code, all_employee

        result = {}
        all_employee = {employee['name']: employee['employees_pk_id'] for employee in all_employee}

        for employee, index in Form.Records.items():
            if employee not in all_employee:
                result[employee] = 404, "Target Employee Not Found"
                continue

            for i, detail in index:
                OBJ = dbm.fingerprint_scanner_form()

                OBJ.employee_fk_id = Form.Records[employee]
                OBJ.created_by_fk_id = Form.created_by_fk_id
                OBJ.In_Out = detail['In_Out']
                OBJ.Antipass = detail['Antipass']
                OBJ.ProxyWork = detail['ProxyWork']
                OBJ.DateTime = detail['DateTime']
                db.add(OBJ)
                db.commit()
                db.refresh(OBJ)
        return 200, result
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


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
        return 500, e.__repr__()


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

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


'''
[
  {
    "priority": 5,
    "visible": true,
    "create_date": "2024-02-07T11:07:42.427019+00:00",
    "update_date": null,
    "can_deleted": true,
    "created_by_fk_id": null,
    "name": "string",
    "job_title": "teacher",
    "employees_pk_id": "671ef1bd-17f8-4898-ad10-05ffaf8c6271",
    "last_name": "string",
    "expire_date": null,
    "can_update": true,
    "deleted": false,
    "delete_date": null
  },
  {
    "priority": 5,
    "visible": true,
    "create_date": "2024-02-07T11:07:45.843458+00:00",
    "update_date": null,
    "can_deleted": true,
    "created_by_fk_id": null,
    "name": "string",
    "job_title": "teacher",
    "employees_pk_id": "20545185-406a-425d-864d-6a2c619c6d59",
    "last_name": "string",
    "expire_date": null,
    "can_update": true,
    "deleted": false,
    "delete_date": null
  },
  {
    "priority": 5,
    "visible": true,
    "create_date": "2024-02-07T11:07:46.534765+00:00",
    "update_date": null,
    "can_deleted": true,
    "created_by_fk_id": null,
    "name": "string",
    "job_title": "teacher",
    "employees_pk_id": "8447d4a0-5da6-470e-b52f-5619693aece9",
    "last_name": "string",
    "expire_date": null,
    "can_update": true,
    "deleted": false,
    "delete_date": null
  },
  {
    "priority": 5,
    "visible": true,
    "create_date": "2024-02-07T11:07:47.149447+00:00",
    "update_date": null,
    "can_deleted": true,
    "created_by_fk_id": null,
    "name": "string",
    "job_title": "teacher",
    "employees_pk_id": "3afbfa3a-17d7-4001-83a0-260310f27e7c",
    "last_name": "string",
    "expire_date": null,
    "can_update": true,
    "deleted": false,
    "delete_date": null
  }
]


'''