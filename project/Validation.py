from pydantic import BaseModel
from datetime import date


class BASE_Employee(BaseModel):
    name: str
    last_name: str
    job_title: str


class BASE_Leave_Form(BaseModel):
    id: int
    employee_id: int
    start: date
    end: date
    Description: str