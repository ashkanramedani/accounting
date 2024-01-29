from sqlalchemy.orm import Session
from datetime import datetime
import sqlalchemy.sql.expression as sse
import logging
import schemas as sch
import db.models as dbm
from sqlalchemy import desc, asc
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
