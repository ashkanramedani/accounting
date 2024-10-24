from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def get_all_cluster(db: Session):
    try:
        return 200, [dict(name)["cluster"] for name in db.query(dbm.Role_form.cluster).group_by(dbm.Role_form.cluster).all()]
        # return record_order_by(db,dbm.Tag_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


# role

def get_role(db: Session, role_id):
    try:
        return 200, db.query(dbm.Role_form).filter_by(role_pk_id=role_id).filter(dbm.Role_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_role(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Role_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_role(db: Session, Form: sch.post_role_schema):
    try:

        data = Form.dict()
        if data["name"] == "Administrator":
            return 400, "illegal name Administrator"

        OBJ = dbm.Role_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_role(db: Session, role_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Role_form).filter_by(role_pk_id=role_id).filter(dbm.Role_form.status != "deleted").first()
        if not record:
            return 400, "Role Record Not Found"
        if record.name == "Administrator":
            return 400, "Administrator role cant be deleted"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_role(db: Session, Form: sch.update_role_schema):
    try:
        record = db.query(dbm.Role_form).filter_by(role_pk_id=Form.role_pk_id).filter(dbm.Role_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        data = Form.dict()
        if data["name"] == "Administrator":
            return 400, "illegal name Administrator"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_role_status(db: Session, role_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Role_form).filter_by(role_pk_id=role_id).first()
        if not record:
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
