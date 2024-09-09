from pydantic import root_validator

from ..Base import *


class Discount_Type(str, Enum):
    percentage = 'percentage'
    fix = 'fix'


class discount_code(Base_form):
    pass

    class Config:
        extra = 'ignore'


class post_discount_code_schema(discount_code):
    discount_type: Discount_Type
    discount_amount: float

    @root_validator(pre=True)
    def flatten_type(cls, values):
        if values['discount_type'] == Discount_Type.percentage or values['discount_type'] == 'percentage':
            values['discount_amount'] = min(values['discount_amount'], 100)
        return values
    class Config:
        extra = 'ignore'


class update_discount_code_schema(discount_code):
    discount_code_pk_id: UUID

    class Config:
        extra = 'ignore'


class discount_code_response(Base_response, update_discount_code_schema):
    discount_code: str

    class Config:
        extra = 'ignore'
        orm_mode = True
