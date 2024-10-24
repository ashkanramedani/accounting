from ..Base import *


class User(Entity, Base_form):
    fingerprint_scanner_user_id: int
    roles: Optional[List[Update_Relation]] = []


class post_user_schema(User):
    pass


class update_user_schema(User):
    user_pk_id: UUID


class user_response(Entity_Response):
    user_pk_id: UUID
    roles: List[export_role] | None
    fingerprint_scanner_user_id: Optional[int | str] = None

    class Config:
        extra = 'ignore'
        orm_mode = True