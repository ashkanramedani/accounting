from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True

def Fix_UUID(hex_string):
    if isinstance(hex_string, UUID):
        return hex_string
    return UUID(hex_string)

