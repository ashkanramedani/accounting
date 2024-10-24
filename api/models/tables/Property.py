from sqlalchemy.orm import relationship

from .Base_form import *


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
