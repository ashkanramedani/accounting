from ..Base import *


class payment_method(Base_form):
    shaba: str
    card_number: str

    class Config:
        extra = 'ignore'

class post_payment_method_schema(payment_method):
    user_fk_id: UUID

    class Config:
        extra = 'ignore'

class update_payment_method_schema(payment_method):
    payment_method_pk_id: UUID

    class Config:
        extra = 'ignore'

class payment_method_response(Base_response, update_payment_method_schema):
    employee: export_employee

    class Config:
        extra = 'ignore'
        orm_mode = True
