from .Base import *


class Role(Base_form):
    name: str
    cluster: str



class post_role_schema(Role):
    pass


class update_role_schema(Role):
    role_pk_id: UUID


class role_response(update_role_schema):
    created: export_employee

    class Config:
        orm_mode = True


class fingerprint_scanner(Base_form):
    user_fk_id: UUID
    Date: date | str
    Enter: time | str | None
    Exit: time | str | None


class post_fingerprint_scanner_schema(fingerprint_scanner):
    pass


class update_fingerprint_scanner_schema(fingerprint_scanner):
    fingerprint_scanner_pk_id: UUID

class fingerprint_scanner_response(Base_response):
    fingerprint_scanner_pk_id: UUID
    Date: date | str
    Enter: time | str | None
    Exit: time | str | None
    EnNo: int
    created: export_employee

    class Config:
        orm_mode = True


class payment_method(Base_form):
    user_fk_id: UUID
    shaba: str
    card_number: str


class post_payment_method_schema(payment_method):
    pass


class update_payment_method_schema(payment_method):
    payment_method_pk_id: UUID


class payment_method_response(Base_response, update_payment_method_schema):
    employee: export_employee

    class Config:
        orm_mode = True
