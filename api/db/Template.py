from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *


def get_template(db: Session, form_id):
    try:
        return 200, db.query(dbm.Template_form).filter_by(template_pk_id=form_id).filter(dbm.Template_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_template(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Template_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_template(db: Session, Form: sch.post_template_schema):
    try:
        OBJ = dbm.Template_form(**Form.__dict__)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 201, OBJ

    except Exception as e:
        return Return_Exception(db, e)


def delete_template(db: Session, template_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Template_form).filter_by(template_pk_id=template_id).filter(dbm.Template_form.status != "deleted").first()
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_template(db: Session, Form: sch.update_template_schema):
    try:
        record = db.query(dbm.Template_form).filter_by(template_pk_id=Form.template_pk_id).filter(dbm.Template_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()

        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_template_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Template_form).filter_by(template_pk_id=form_id).first()
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
