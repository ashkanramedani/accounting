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

class Employee(Entity):
    priority: int | None
    fingerprint_scanner_user_id: int | None = None
    roles: List[UUID] | None = []


class post_employee_schema(Employee):
    pass


class update_employee_schema(Entity):
    employees_pk_id: UUID
    priority: int | None
    fingerprint_scanner_user_id: int | None = None


class employee_response(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    roles: List[export_role] | None

    class Config:
        orm_mode = True



# ---------------------- student ----------------------
class Student(Entity):
    created_fk_by: UUID
    level: str


class post_student_schema(Student):
    pass


class update_student_schema(Student):
    student_pk_id: UUID


class student_response(update_student_schema):
    created: export_employee

    class Config:
        orm_mode = True