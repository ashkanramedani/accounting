from ..Base import *

class Employee(Entity, Base_form):
    fingerprint_scanner_user_id: Optional[int] = None
    roles: Optional[List[Update_Relation]] = []


class post_employee_schema(Employee):
    pass


class update_employee_schema(Employee):
    user_pk_id: UUID


class employee_response(Entity):
    user_pk_id: UUID
    roles: List[export_role] | None
    fingerprint_scanner_user_id: Optional[int | str] = None

    class Config:
        orm_mode = True
