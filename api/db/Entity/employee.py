from typing import List

from sqlalchemy.orm import Session, joinedload

import models as dbm
import schemas as sch
from ..Extra import *


def get_employee(db: Session, employee_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=employee_id, is_employee=True).filter(dbm.User_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_employee(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        query = db.query(dbm.User_form).filter(dbm.User_form.status != "deleted").options(joinedload(dbm.User_form.roles))
        return record_order_by(db, dbm.User_form, page, limit, order, SortKey, query=query)
    except Exception as e:
        return Return_Exception(db, e)


def post_employee(db: Session, Form: sch.post_employee_schema):
    try:
        Warn = []
        data = Form.dict()
        roles: List[sch.Update_Relation | str] | str = data.pop("roles") if "roles" in data else None

        if data["name"] == "Admin":
            return 400, "illegal Name Admin"

        OBJ = dbm.User_form(**data, is_employee=True)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if roles:
            Warn = Add_role(db, roles, OBJ, OBJ.user_pk_id)
        return 201, sch.Base_record_add(Warning=' | '.join(Warn), id=Primary_key(OBJ))

    except Exception as e:
        return Return_Exception(db, e)


def delete_employee(db: Session, employee_id, deleted_by=None):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=employee_id).filter(dbm.User_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        if record.name == "Admin":
            return 400, "Admin Cont be deleted"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_employee(db: Session, Form: sch.update_employee_schema):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=Form.user_pk_id).filter(dbm.User_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        if data["name"] == "Admin":
            return 400, "illegal Name Admin"

        roles: List[sch.Update_Relation | str] | str = data.pop("roles") if "roles" in data else None
        record.update(data, synchronize_session=False)
        db.commit()

        if not roles:
            return 200, "Record Updated"

        Error = Add_role(db, roles, record.first(), Form.user_pk_id)
        if Error:
            return 200, "Record Updated But there was an error in roles: " + " | ".join(Error)
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_employee_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=form_id, is_employee=False).first()
        if not record.first():
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
