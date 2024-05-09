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
    priority: Optional[int] = 5
    fingerprint_scanner_user_id: Optional[int] = None
    roles: Optional[List[Update_Relation]] = []


class post_employee_schema(Employee):
    pass


class update_employee_schema(Employee):
    roles: Optional[List[Update_Relation]] = []
    user_pk_id: UUID

    

class employee_response(Entity):
    user_pk_id: UUID
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
