from sqlalchemy import Date, Float, case, TIME, DATE
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .Base_form import *


class Leave_Request_form(Base, Base_form):
    __tablename__ = "leave_request"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    leave_request_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")
    user_fk_id = create_foreignKey("User_form")

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    leave_type = Column(String, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Business_Trip_form(Base, Base_form):
    __tablename__ = "business_trip"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    business_trip_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    destination = Column(String, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Remote_Request_form(Base, Base_form):
    __tablename__ = "remote_request"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    remote_request_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")

    working_location = Column(String, nullable=False)

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Payment_Method_form(Base, Base_form):
    __tablename__ = "payment_method"
    __table_args__ = (UniqueConstraint('user_fk_id', 'shaba', 'card_number'),)

    payment_method_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")
    shaba = Column(String(24), nullable=False, unique=True)
    card_number = Column(String(16), nullable=True, unique=True)
    active = Column(Boolean, default=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Fingerprint_Scanner_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner"
    __table_args__ = (UniqueConstraint('EnNo', 'Date', 'Enter', 'Exit'),)

    fingerprint_scanner_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    EnNo = Column(Integer, nullable=False, index=True)
    Date = Column(DATE, nullable=False, index=True)
    Enter = Column(TIME, nullable=False, index=True)
    Exit = Column(TIME, nullable=True, index=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])

    @hybrid_property
    def valid(self):
        return self.Enter is not None and self.Exit is not None

    @valid.expression
    def valid(self):
        return case(
                [(self.Enter.isnot(None) & self.Exit.isnot(None), True)],
                else_=False)

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Fingerprint_Scanner_backup_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner_backup"
    __table_args__ = (UniqueConstraint('EnNo', 'DateTime'),)

    fingerprint_scanner_backup_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    TMNo = Column(Integer, nullable=False, index=True)
    EnNo = Column(Integer, nullable=False, index=True)
    GMNo = Column(Integer, nullable=False, index=True)
    Mode = Column(String)
    In_Out = Column(String)
    Antipass = Column(Integer)
    ProxyWork = Column(Integer)
    DateTime = Column(DateTime, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])

    # ++++++++++++++++++++++++++ TeacherBase +++++++++++++++++++++++++++

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teacher_Tardy_report_form(Base, Base_form):
    __tablename__ = "teacher_tardy_report"
    __table_args__ = (UniqueConstraint('teacher_fk_id', 'session_fk_id', 'delay'),)

    teacher_tardy_report_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")

    teacher_fk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    delay = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[teacher_fk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    session = relationship("Session_form", foreign_keys=[session_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Sub_Request_form(Base, Base_form):
    __tablename__ = "sub_request"

    sub_request_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")

    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    main_teacher_fk_id = create_foreignKey("User_form")
    sub_teacher_fk_id = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    sessions = relationship("Session_form", foreign_keys=[session_fk_id])
    main_teacher = relationship("User_form", foreign_keys=[main_teacher_fk_id])
    sub_teacher = relationship("User_form", foreign_keys=[sub_teacher_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Session_Cancellation_form(Base, Base_form):
    __tablename__ = "session_cancellation"

    session_cancellation_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")

    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    session = relationship("Session_form", foreign_keys=[session_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Role_form(Base, Base_form):
    __tablename__ = "role"

    role_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")

    name = Column(String, index=True, nullable=False, unique=True)
    cluster = Column(String, index=True, nullable=False)
    value = Column(Float, default=0.0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    users = relationship('User_form', secondary=UserRole, back_populates='roles')

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)

    # ++++++++++++++++++++++++++ Salary_Policy_form +++++++++++++++++++++++++++
