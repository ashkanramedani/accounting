import datetime
import email
# from enum import unique
# from unicodedata import category
# from click import style
from typing import List, Union
from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, BigInteger, Date, Time, UniqueConstraint, Index, MetaData, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import expression, func
from email.policy import default
from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

metadata_obj = MetaData()

__all__ = [
    "Student",
    "Employees",
    "Leave_Request",
    "Teacher_Tardy_Reports",
    "Survey_Question",
    "Survey",
    "Teachers_Report",
    "Class_Cancellation",
    "Teacher_Replacement",
    "Employee_Timesheet",
    "Business_Trip",
    "Remote_Request"]


# PK

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

class Employees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    job_title = Column(String, index=True)

class Leave_Request(Base):
    __tablename__ = "leave_request"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    Start_Date = Column(Date, index=True)
    End_Date = Column(Date, index=True)
    Description = Column(String)

# class Survey(Base):
#     __tablename__ = "survey"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
#     Question_list = Column()
#     Description: str

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)

    # Define a one-to-many relationship with the Question table
    questions = relationship("Question", back_populates="survey")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String)

    # Define the foreign key relationship with the Survey table
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="questions")

class Servey_Relation(Base):
    __tablename__ = "servey_relation"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Survey_id = Column(Integer, ForeignKey("surveys.id"), index=True, unique=False)
    Survey_Question_id = Column(Integer, ForeignKey("servey_question.id"), index=True, unique=False)


class Survey_Question(Base):
    __tablename__ = "servey_question"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String)

# class Teacher_Tardy_Reports(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)



# class Teachers_Report(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# class Class_Cancellation(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# class Teacher_Replacement(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# class Employee_Timesheet(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# class Business_Trip(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)


# class Remote_Request(Base):
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)