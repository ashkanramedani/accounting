from .Base import *

__all__ = [
    "Employee",
    "post_employee_schema",
    "update_employee_schema",
    "employee_response",
    "export_employee",
    "Student",
    "post_student_schema",
    "update_student_schema",
    "student_response"]


# ---------------------- Employee ----------------------

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


# ---------------------- student ----------------------
class Student(Entity, Base_form):
    pass


class post_student_schema(Student):
    pass


class update_student_schema(Student):
    user_pk_id: UUID


class student_response(BaseModel):
    description: str | None = None
    status: int = 0
    user_pk_id: UUID
    name: str
    last_name: str
    level: str
    day_of_birth: date | datetime | str

    class Config:
        orm_mode = True
