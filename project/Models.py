from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from typing import List

from sqlalchemy.orm import relationship

from Connector import PSQL

__all__ = [
    "Student",
    "employees",
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


class Student(PSQL):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class employees(PSQL):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    job_title = Column(String, index=True)


class Leave_Request(PSQL):
    __tablename__ = "leave_request"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    Start_Date = Column(Date, index=True)
    End_Date = Column(Date, index=True)
    Description = Column(String)


class Teacher_Tardy_Reports(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Survey(PSQL):
    __tablename__ = "survey"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    Question_list = Column()
    Description: str


class Servey_Relation(PSQL):
    __tablename__ = "servey_relation"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Survey_id = Column(Integer, ForeignKey("servey.id"), index=True, unique=False)
    Survey_Question_id = Column(Integer, ForeignKey("servey_question.id"), index=True, unique=False)


class Survey_Question(PSQL):
    __tablename__ = "servey_question"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String)


class Teachers_Report(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Class_Cancellation(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Teacher_Replacement(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Employee_Timesheet(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Business_Trip(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Remote_Request(PSQL):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Survey(PSQL):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)

    # Define a one-to-many relationship with the Question table
    questions = relationship("Question", back_populates="survey")


class Question(PSQL):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String)

    # Define the foreign key relationship with the Survey table
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="questions")
