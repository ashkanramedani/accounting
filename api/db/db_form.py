from sqlalchemy.orm import Session
from datetime import datetime
import sqlalchemy.sql.expression as sse
import logging
import api.schemas as sch
import models as dbm
from sqlalchemy import desc, asc
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def post_data(db: Session, Form):
    try:
        data = db.query(dbm.Employees).filter(dbm.Employees.id == Form.id)
        OBJ = dbm.Leave_form(
            id=Form.id,
            employee_id=Form.employee_id,
            Start_Date=Form.start,
            End_Date=Form.end,
            Description=Form.Description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
    except Exception as e:
        logging.error(e)
        db.rollback()
        return -1 