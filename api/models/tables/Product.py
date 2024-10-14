from random import randint

from sqlalchemy import Float, DATE
from sqlalchemy.orm import relationship

from .Base_form import *


class Products_Mapping_form(Base, Base_form):
    __tablename__ = "products_mapping"
    # __table_args__ = (UniqueConstraint('product_mapping_pk_id', 'target_product_fk_id'),)

    products_mapping_pk_id = create_Unique_ID()
    target_product_fk_id = Column(GUID, nullable=False, unique=False, index=True)
    target_product_table = Column(String, nullable=True, index=True)

    product_name = Column(String, nullable=False, index=True)
    product_quantity = Column(Integer, default=0)
    product_price = Column(Float, nullable=False)
    product_discounted_price = Column(Float, nullable=False)


class Seasonal_Discount_form(Base, Base_form):
    __tablename__ = "seasonal_discount"

    seasonal_discount_pk_id = create_Unique_ID()
    target_product_fk_id = create_foreignKey("Products_Mapping_form")
    discount_type = Column(String, nullable=False, index=True)  # Fix / Percentage
    discount_amount = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=False)


class Shopping_card_form(Base, Base_form):
    __tablename__ = "shopping_card"
    shopping_card_pk_id = create_Unique_ID()
    card_id = Column(String, nullable=False)
    user_fk_id = create_foreignKey("User_form")
    transaction_fk_id = create_foreignKey("Transaction_form", nullable=True)
    discount_fk_id = create_foreignKey("Discount_code_form", nullable=True)

    # bucket = Column(JSON, nullable=False, default={})
    total = Column(Float, nullable=False, default=0)
    total_discounted = Column(Float, nullable=False, default=0)

    transaction = relationship("Transaction_form", foreign_keys=[transaction_fk_id])


class Shopping_card_item_form(Base):
    __tablename__ = "shopping_card_item"

    shopping_card_item_pk_id = create_Unique_ID()
    shopping_card_fk_id = create_foreignKey("Shopping_card_form")
    product_fk_id = create_foreignKey("Products_Mapping_form")

    quantity = Column(Integer, nullable=False, default=1)
    expire_date = Column(DateTime, default=None)


class Discount_code_form(Base, Base_form):
    __tablename__ = "discount_code"
    discount_code_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    target_user_fk_id = create_foreignKey("User_form", nullable=True)
    target_product_fk_id = create_foreignKey("Products_Mapping_form", nullable=True)

    discount_code = Column(String, nullable=False, index=True)
    discount_type = Column(String, nullable=False, index=True)  # Fix / Percentage
    discount_amount = Column(Float, nullable=False)

    start_date = Column(DATE, nullable=True, index=True, default=None)
    end_date = Column(DATE, nullable=True, index=True, default=None)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    target_user = relationship("User_form", foreign_keys=[target_user_fk_id])
    target_product = relationship("Products_Mapping_form", foreign_keys=[target_product_fk_id])


class Discount_code_usage_form(Base, Base_form):
    __tablename__ = "discount_code_usage"

    discount_code_usage_pk_id = create_Unique_ID()

    user_fk_id = create_foreignKey("User_form")
    discount_code_fk_id = create_foreignKey("Discount_code_form")

    user = relationship("User_form", foreign_keys=[user_fk_id])
    discount_code = relationship("Discount_code_form", foreign_keys=[discount_code_fk_id])


class Transaction_form(Base, Base_form):
    __tablename__ = "transaction"

    transaction_pk_id = create_Unique_ID()

    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False, default="IRR")
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=False)

    Token = Column(String, nullable=True, index=True)
    data = Column(JSON, nullable=True)
