from schemas.Base import *



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

    class Config:
        orm_mode = True
