import pstats
from fastapi import Query, Body
from datetime import datetime
from typing import List, Union, Optional, Dict
from datetime import datetime, time, timedelta, date

from uuid import UUID
from typing import Optional, List, Dict, Any

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

from pydantic import BaseModel

class Employee_schema(BaseModel):
    name: str
    last_name: str
    job_title: str


class Leave_request_schema(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    Description: str
