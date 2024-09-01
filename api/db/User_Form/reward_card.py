from sqlalchemy.orm import Session

import schemas as sch
import models as dbm
from db.Extra import *


def get_reward_card(db: Session, reward_card_id):
    try:
        return 200, db.query(dbm.Reward_card_form).filter_by(reward_card_pk_id=reward_card_id).filter(dbm.Reward_card_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_reward_card(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Reward_card_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_reward_card(db: Session, Form: sch.post_reward_card_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by, Form.user_fk_id]):
            return 400, "Bad Request"

        OBJ = dbm.Reward_card_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "reward_card Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_reward_card(db: Session, reward_card_id):
    try:
        record = db.query(dbm.Reward_card_form).filter_by(reward_card_pk_id=reward_card_id).filter(dbm.Reward_card_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_reward_card(db: Session, Form: sch.update_reward_card_schema):
    try:
        record = db.query(dbm.Reward_card_form).filter_by(reward_card_pk_id=Form.reward_card_pk_id)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)
