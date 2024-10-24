import functools

from sqlalchemy import Boolean, String, DateTime, MetaData, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base

# from models.tables.User import User_form
from models.Func import *

Base = declarative_base()
metadata_obj = MetaData()


class Base_form:
    priority = Column(Integer, default=5, nullable=True)

    visible = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False, index=True)
    can_update = Column(Boolean, default=True, nullable=False)
    can_deleted = Column(Boolean, default=True, nullable=False)

    create_date = Column(DateTime, default=IRAN_TIME(dump=True), nullable=False, index=True)
    update_date = Column(DateTime, default=None, onupdate=IRAN_TIME(dump=True))
    expire_date = Column(DateTime, default=None)

    description = Column(String, nullable=True, default="")
    note = Column(JSON, nullable=True, default={})

    status = Column(String, nullable=False, default="submitted", index=True)  # NC: 006


UserRole = association_table(Base, "User_form", "Role_form")
CourseTag = association_table(Base, "Course_form", "Tag_form")
CourseCategory = association_table(Base, "Course_form", "Category_form")
