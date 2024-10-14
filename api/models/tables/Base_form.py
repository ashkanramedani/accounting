from sqlalchemy import Boolean, Integer, String, DateTime, Table, UniqueConstraint, MetaData
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


survey_questions = Table(
        "survey_questions",
        Base.metadata,
        Column("survey_fk_id", ForeignKey("survey.survey_pk_id")),
        Column("question_fk_id", ForeignKey("question.question_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("survey_fk_id", "question_fk_id", "deleted"), )

UserRole = Table(
        "users_roles",
        Base.metadata,
        Column("user_fk_id", ForeignKey("user.user_pk_id")),
        Column("role_fk_id", ForeignKey("role.role_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("user_fk_id", "role_fk_id", "deleted"), )

CourseTag = Table(
        "course_tag",
        Base.metadata,
        Column("tag_fk_id", ForeignKey("tag.tag_pk_id")),
        Column("course_fk_id", ForeignKey("course.course_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("tag_fk_id", "course_fk_id", "deleted"), )

CourseCategory = Table(
        "course_category",
        Base.metadata,
        Column("category_fk_id", ForeignKey("category.category_pk_id")),
        Column("course_fk_id", ForeignKey("course.course_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("category_fk_id", "course_fk_id", "deleted"),
)
