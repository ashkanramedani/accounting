from schemas.Base import *


class fingerprint_scanner(Base_form):
    Enter: time | str
    Exit: time | str


class post_fingerprint_scanner_schema(fingerprint_scanner):
    Date: date | str
    user_fk_id: UUID


class update_fingerprint_scanner_schema(fingerprint_scanner):
    fingerprint_scanner_pk_id: UUID


class fingerprint_scanner_response(Base_response):
    fingerprint_scanner_pk_id: UUID
    Date: date | str
    Enter: time | str | None = TIME_NOW()
    Exit: time | str | None = TIME_NOW()
    EnNo: int

    class Config:
        extra = 'ignore'
        orm_mode = True


class FingerPrint_report(BaseModel):
    Invalid: int
    TotalHour: int
    Fingerprint_scanner_report: List
    # Fingerprint_scanner_report: List[fingerprint_scanner_response]
