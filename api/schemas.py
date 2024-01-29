import pstats
from fastapi import Query, Body
from datetime import datetime
from typing import List, Union, Optional, Dict
from datetime import datetime, time, timedelta, date

from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

from pydantic import BaseModel

class BASE_Employee(BaseModel):
    id: int
    name: str
    last_name: str
    job_title: str


class BASE_Leave_Form(BaseModel):
    id: int
    employee_id: int
    start: date
    end: date
    Description: str