from typing import List
from uuid import UUID

from lib import logger


from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from .Extra import *


def get_employee(db: Session, employee_id):
    try:
        return 200, db.query(dbm.Employees_form).filter_by(employees_pk_id=employee_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_employee(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Employees_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        data = Form.dict()
        roles: List[UUID] = data.pop("roles")

        OBJ = dbm.Employees_form(**data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if not roles:
            return 200, f'Employee Added. ID: {OBJ.employees_pk_id}'

        role_ID: List[UUID] = [ID.role_pk_id for ID in db.query(dbm.Roles_form).filter_by(deleted=False).all()]

        for r_id in roles:
            if r_id not in role_ID:
                return 400, "Bad Request"
            OBJ.roles.append(db.query(dbm.Roles_form).filter_by(role_pk_id=r_id, deleted=False).first())
        db.commit()

        return 200, f'Employee Added. ID: {OBJ.employees_pk_id}'
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_employee(db: Session, employee_id):
    try:
        record = db.query(dbm.Employees_form).filter_by(employees_pk_id=employee_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.Employees_form).filter_by(employees_pk_id=Form.employees_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.warning(e)
        db.rollback()
        return 500, e.__repr__()
