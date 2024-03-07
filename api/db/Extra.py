from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm

__all__ = ["employee_exist", "class_exist"]


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True


def class_exist(db: Session, FK_field: UUID):
    if not db.query(dbm.Class_form).filter_by(class_pk_id=FK_field, deleted=False).first():
        return False
    return True
