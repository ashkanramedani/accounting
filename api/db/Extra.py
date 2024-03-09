from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch

__all__ = ["employee_exist", "class_exist", 'record_order_by']


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True


def class_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.Class_form).filter_by(class_pk_id=FK_field, deleted=False).first():
        return False
    return True


def record_order_by(db: Session, table, page: sch.PositiveInt, limit: sch.PositiveInt, order: str):
    if order == "desc":
        return 200, db.query(table).filter_by(deleted=False).order_by(table.create_date.desc()).offset((page - 1) * limit).limit(limit).all()
    return 200, db.query(table).filter_by(deleted=False).order_by(table.create_date.asc()).offset((page - 1) * limit).limit(limit).all()
