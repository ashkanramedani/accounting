from datetime import timezone, datetime

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


def get_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(
                employees_pk_id=employee_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def get_all_employee(db: Session):
    try:
        data = db.query(dbm.Employees_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        OBJ = dbm.Employees_form()

        OBJ.name = Form.name
        OBJ.last_name = Form.last_name
        OBJ.job_title = Form.job_title
        OBJ.priority = Form.priority
        OBJ.fingerprint_scanner_pk_id = Form.user_ID

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Employee Added"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def delete_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(
                employee_id=employee_id,
                deleted=False
        ).first()
        if not record or record.deleted:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.args[0]


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.Employees_form).filter(dbm.Employees_form.employees_pk_id == Form.employees_pk_id).first()
        if not record or record.deleted:
            return 404, "Not Found"
        record.name = Form.name,
        record.last_name = Form.last_name,
        record.job_title = Form.job_title
        record.update_date = datetime.now(timezone.utc).astimezone()

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.args[0]
