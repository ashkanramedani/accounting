from typing import Literal
from pydantic import root_validator
from ..Base import *


class discount_code(Base_form):
    pass

    class Config:
        extra = 'ignore'


class post_discount_code_schema(discount_code):
    discount_type: str = Literal["percentage", "fix"]
    discount_amount: float

    target_user_fk_id: Optional[UUID] = None
    target_product_fk_id: Optional[UUID] = None

    start_date: date | str
    end_date: date | str

    @root_validator(pre=True)
    def flatten_type(cls, values):
        if values['discount_type'] == 'percentage':
            values['discount_amount'] = min(values['discount_amount'], 100)
        return values

    class Config:
        extra = 'ignore'


class update_discount_code_schema(discount_code):
    discount_code_pk_id: UUID

    class Config:
        extra = 'ignore'


class discount_code_response(Base_response):
    discount_code_pk_id: UUID
    discount_code: str

    target_user: Optional[UUID] = None
    target_product: Optional[UUID] = None

    class Config:
        extra = 'ignore'
        orm_mode = True


class apply_code(BaseModel):
    price: float
    discount_code: str

    target_user: Optional[UUID] = None
    target_product: Optional[UUID] = None

    class Config:
        extra = 'ignore'
        orm_mode = True
