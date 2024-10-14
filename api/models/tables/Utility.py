from sqlalchemy import Float, Date
from sqlalchemy.orm import relationship

from .Base_form import *


class Template_form(Base, Base_form):
    __tablename__ = "templates"
    template_pk_id = create_Unique_ID()
    template_table = Column(String, index=True, nullable=False)
    template_name = Column(String, index=True, nullable=False)
    data = Column(JSON, nullable=False)


class Status_form(Base, Base_form):  # NC: 002
    __tablename__ = "status"
    __table_args__ = (UniqueConstraint('status_name', 'status_cluster'),)

    status_pk_id = create_Unique_ID()

    status_name = Column(String, index=True, nullable=False)
    status_cluster = Column(String, index=True, nullable=False)

    created_fk_by = create_foreignKey("User_form", nullable=True)
    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Deleted_Records(Base):
    __tablename__ = "deleted_records"
    deleted_records_pk_id = create_Unique_ID()
    deleted_fk_by = create_foreignKey("User_form", nullable=True)
    table = Column(String, nullable=False)
    rows_data = Column(JSON, nullable=False)


class Reward_card_form(Base, Base_form):
    __tablename__ = "reward_card"

    reward_card_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")
    reward_amount = Column(Float, nullable=False)
    reward_type = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])


class Status_history(Base):
    __tablename__ = "status_history"

    status_history_pk_id = create_Unique_ID()

    status = Column(String, nullable=False, index=True)
    table_name = Column(String, nullable=False, index=True)
    create_date = Column(DateTime, default=IRAN_TIME, nullable=False, index=True)
