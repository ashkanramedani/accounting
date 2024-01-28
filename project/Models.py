from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from Connector import PSQL


class Employee(PSQL):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    job_title = Column(String, index=True)


class Leave_form(PSQL):
    __tablename__ = "leave_form"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    Start_Date = Column(Date, index=True)
    End_Date = Column(Date, index=True)
    Description = Column(String)
