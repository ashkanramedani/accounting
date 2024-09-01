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


def delete_template(db: Session, template_id):
    try:
        record = db.query(dbm.Template_form).filter_by(template_pk_id=template_id).filter(dbm.Template_form.status != "deleted").first()
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
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
