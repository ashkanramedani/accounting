from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

import models as dbm
import schemas as sch
from ..Extra import *


def user_dropdown(db: Session, order, SortKey, is_employee):
    try:
        return record_order_by(db, dbm.User_form, 0, 0, order, SortKey, is_employee=is_employee)
    except Exception as e:
        return Return_Exception(db, e)


def get_by_role(db: Session, role: str, page: sch.NonNegativeInt, limit: sch.PositiveInt=10, order: str = "desc", SortKey: str = None):
    try:
        query = db.query(dbm.User_form).options(joinedload(dbm.User_form.roles))

        if SortKey:
            if SortKey not in dbm.User_form.__table__.columns.keys():
                return Return_Exception(db, ValueError(f"Invalid key: {SortKey}"))

        TargetColumn = getattr(dbm.User_form, SortKey) if SortKey else dbm.User_form.create_date
        if order == "asc":
            query = query.order_by(TargetColumn)
        else:
            query = query.order_by(desc(TargetColumn))

        targets = [
            user
            for user in query.all()
            if role in [role.cluster.lower() for role in user.roles]]

        if page > 0:
            start = (page - 1) * limit
            targets = targets[start: start + limit]
        return 200, targets
    except Exception as e:
        return Return_Exception(db, e)


def get_user(db: Session, user_id):
    try:
        return 200, db.query(dbm.User_form).filter_by(user_pk_id=user_id).filter(dbm.User_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_user(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.User_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_user(db: Session, Form: sch.post_user_schema):
    try:
        OBJ = dbm.User_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "user Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_user(db: Session, user_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=user_id).filter(dbm.User_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "user Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_user(db: Session, Form: sch.update_user_schema):
    try:
        record = db.query(dbm.User_form).filter(dbm.User_form.user_pk_id == Form.user_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_user_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=form_id).first()
        if not record:
            return 404, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
