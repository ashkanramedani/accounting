from sqlalchemy.orm import Session

import models as dbm
from ..Extra import *


def user_dropdown(db: Session, order, SortKey, is_employee):
    try:
        return record_order_by(db, dbm.User_form, 0, 0, order, SortKey, is_employee=is_employee)
    except Exception as e:
        return Return_Exception(db, e)
