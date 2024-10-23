from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

import models as dbm
from ..Extra import *

from lib import logger
import schemas as sch


def user_dropdown(db: Session, order, SortKey, is_employee):
    try:
        return record_order_by(db, dbm.User_form, 0, 0, order, SortKey, is_employee=is_employee)
    except Exception as e:
        return Return_Exception(db, e)


def get_by_role(db: Session, role: str, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
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
            if role in [role.name.lower() for role in user.roles]]

        if page > 0:
            start = (page - 1) * limit
            targets = targets[start: start + limit]
        return 200, targets
    except Exception as e:
        return Return_Exception(db, e)
