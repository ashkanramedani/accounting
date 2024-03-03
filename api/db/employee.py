from datetime import timezone, datetime

from loguru import logger
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch


def get_employee(db: Session, employee_id):
    try:
        return 200, db.query(dbm.Employees_form).filter_by(employees_pk_id=employee_id, deleted=False).first()
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def get_all_employee(db: Session):
    try:
        return 200, db.query(dbm.Employees_form).filter_by(deleted=False).all()
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        OBJ = dbm.Employees_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Employee Added"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def delete_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(employee_id=employee_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.Employees_form).filter_by(employees_pk_id=Form.employees_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        data["update_date"] = datetime.now(timezone.utc).astimezone()
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
