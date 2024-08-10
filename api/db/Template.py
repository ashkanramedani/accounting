from typing import List

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from db.Extra import *


def get_template(db: Session, form_id):
    try:
        return 200, db.query(dbm.Template_form).filter_by(template_pk_id=form_id).filter(dbm.User_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_template(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.User_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_template(db: Session, Form: sch.post_template_schema):
    try:
        Warn = []
        data = Form.dict()
        roles: List[sch.Update_Relation | str] | str = data.pop("roles") if "roles" in data else None

        if data["name"] == "Admin":
            return 400, "illegal Name Admin"

        OBJ = dbm.User_form(**data, is_template=True)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        if roles:
            Warn = Add_role(db, roles, OBJ, OBJ.user_pk_id)
        return 201, sch.Base_record_add(Warning=' | '.join(Warn), id=Primary_key(OBJ))

    except Exception as e:
        return Return_Exception(db, e)


def delete_template(db: Session, template_id):
    try:
        record = db.query(dbm.User_form).filter_by(user_pk_id=template_id).filter(dbm.User_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        if record.name == "Admin":
            return 400, "Admin Cont be deleted"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_template(db: Session, Form: sch.update_template_schema):
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
