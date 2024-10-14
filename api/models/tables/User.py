from sqlalchemy.orm import relationship

from .Base_form import *


class User_form(Base, Base_form):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('email', 'mobile_number', 'name', "last_name", "is_employee"),)
    user_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form", nullable=True)

    name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    nickname = Column(String, index=True, nullable=True, default="")

    day_of_birth = Column(DateTime, nullable=True)
    email = Column(String(50), nullable=True, index=True)

    mobile_number = Column(String, default='', nullable=False)
    emergency_number = Column(String, default='', nullable=True)

    id_card_number = Column(String, nullable=True)
    address = Column(String(5000), default=None)

    fingerprint_scanner_user_id = Column(Integer, nullable=True, unique=True, default=None, index=True)

    is_employee = Column(Boolean, default=True, nullable=False, index=True)
    level = Column(String, index=True, nullable=True)
    ID_Experience = Column(Integer, default=0, nullable=False)  # total Working time from start

    roles = relationship('Role_form', secondary=UserRole, back_populates='users')

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)
