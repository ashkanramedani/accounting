from typing import List

from sqlalchemy import Date, Float, Time
from sqlalchemy.orm import relationship, Mapped

from .Base_form import *


class Course_form(Base, Base_form):
    __tablename__ = "course"
    __table_args__ = (UniqueConstraint('course_name', 'course_level', 'course_code'),)

    course_pk_id = create_Unique_ID()
    created_fk_by = FK_Column("User_form")
    course_language = FK_Column("Language_form")
    course_type = FK_Column("Course_Type_form")

    course_name = Column(String)
    course_image = Column(String, nullable=True)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)
    course_capacity = Column(Integer, nullable=False)
    course_level = Column(String, nullable=False)
    course_code = Column(String, nullable=False)

    package_discount = Column(Float, nullable=False, default=0.0)
    Course_price = Column(Float, nullable=False)

    tags = relationship("Tag_form", secondary=CourseTag, backref="course_tag")
    categories = relationship("Category_form", secondary=CourseCategory, backref="course_category")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    language: Mapped["Language_form"] = relationship("Language_form", foreign_keys=[course_language])
    type: Mapped["Course_Type_form"] = relationship("Course_Type_form", foreign_keys=[course_type])
    sub_courses: Mapped[List["Sub_Course_form"]] = relationship("Sub_Course_form", back_populates='course')
    sessions: Mapped[List["Session_form"]] = relationship("Session_form", back_populates='course')

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Sub_Course_form(Base, Base_form):
    __tablename__ = "sub_course"
    __table_args__ = (UniqueConstraint('sub_course_name', 'course_fk_id'),)

    sub_course_pk_id = create_Unique_ID()
    course_fk_id = FK_Column("Course_form")
    created_fk_by = FK_Column("User_form")
    sub_course_teacher_fk_id = FK_Column("User_form")

    supervisor_review = Column(JSON, nullable=True)

    sub_course_name = Column(String, unique=True)
    number_of_session = Column(Integer, nullable=False, default=0)
    sub_course_starting_date = Column(Date, nullable=False)
    sub_course_ending_date = Column(Date, nullable=False)

    sub_request_threshold = Column(Integer, nullable=False, default=24)
    sub_course_capacity = Column(Integer, nullable=False)
    sub_course_available_seat = Column(Integer, nullable=False)
    sub_course_price = Column(Float, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[sub_course_teacher_fk_id])
    course: Mapped["Course_form"] = relationship("Course_form", foreign_keys=[course_fk_id], back_populates="sub_courses")
    sessions: Mapped[List["Session_form"]] = relationship("Session_form", back_populates="sub_course")

    # course = relationship("Course_form", foreign_keys=[course_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Session_form(Base, Base_form):
    __tablename__ = "session"
    __table_args__ = (UniqueConstraint('session_date', 'session_starting_time'),)

    session_pk_id = create_Unique_ID()

    created_fk_by = FK_Column("User_form")
    course_fk_id = FK_Column("Course_form")
    sub_course_fk_id = FK_Column("sub_course")
    session_teacher_fk_id = FK_Column("User_form")
    sub_Request = FK_Column("Sub_Request_form", nullable=True)

    is_sub = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)
    session_date = Column(Date, nullable=False, index=True)
    session_starting_time = Column(Time, nullable=False, index=True)
    session_ending_time = Column(Time, nullable=False, index=True)
    session_duration = Column(Integer, nullable=False)
    days_of_week = Column(Integer, nullable=False)
    can_accept_sub = Column(DateTime, nullable=False, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[session_teacher_fk_id])
    course: Mapped["Course_form"] = relationship("Course_form", foreign_keys=[course_fk_id], back_populates="sessions")
    sub_course: Mapped["Sub_Course_form"] = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id], back_populates="sessions")

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Tag_form(Base, Base_form):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint('tag_name', 'tag_cluster'),)

    tag_pk_id = create_Unique_ID()
    tag_name = Column(String, index=True, nullable=False)
    tag_cluster = Column(String, index=True, nullable=True, default="Main")
    created_fk_by = FK_Column("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Category_form(Base, Base_form):
    __tablename__ = "category"
    __table_args__ = (UniqueConstraint('category_pk_id', 'category_name'),)

    category_pk_id = create_Unique_ID()
    category_name = Column(String, index=True, nullable=False, unique=True)
    category_cluster = Column(String, index=True, nullable=True, default="Main")

    created_fk_by = FK_Column("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Language_form(Base, Base_form):
    __tablename__ = "language"

    language_pk_id = create_Unique_ID()
    language_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = FK_Column("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Course_Type_form(Base, Base_form):
    __tablename__ = "course_type"

    course_type_pk_id = create_Unique_ID()
    course_type_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = FK_Column("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class SignUp_queue(Base):
    __tablename__ = "signup_queue"
    __table_args__ = (UniqueConstraint('student_pk_id', 'subcourse_fk_id'),)
    signup_queue_pk_id = create_Unique_ID()
    student_pk_id = Column(GUID, nullable=False, index=True)
    course_fk_id = Column(GUID, nullable=False, index=True)
    subcourse_fk_id = Column(GUID, nullable=False, index=True)


class SignUp_payment_queue_form(Base, Base_form):
    __tablename__ = "signup_payment_queue"
    __table_args__ = (UniqueConstraint('student_pk_id', 'course_fk_id'),)
    signup_queue_pk_id = create_Unique_ID()

    student_pk_id = FK_Column("User_form")
    course_fk_id = FK_Column("Course_form")
    discount_code = FK_Column("Discount_code_form", nullable=True)

    subcourse_fk_ids = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=False)
    package_discount = Column(Float, nullable=False)

    code = relationship("Discount_code_form", foreign_keys=[discount_code])
    student = relationship("User_form", foreign_keys=[student_pk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])


class SignUp_form(Base):
    __tablename__ = "signup"
    __table_args__ = (UniqueConstraint('student_pk_id', 'subcourse_fk_id'),)
    signup_pk_id = create_Unique_ID()

    student_pk_id = FK_Column("User_form")
    course_fk_id = FK_Column("Course_form")
    subcourse_fk_id = FK_Column("Sub_Course_form")

    course = relationship("Course_form", foreign_keys=[course_fk_id])
    student = relationship("User_form", foreign_keys=[student_pk_id])
    subcourse = relationship("Sub_Course_form", foreign_keys=[subcourse_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)
