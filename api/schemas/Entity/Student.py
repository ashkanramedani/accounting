from ..Base import *


class Student(Entity, Base_form):
    pass


class post_student_schema(Student):
    pass


class update_student_schema(Student):
    user_pk_id: UUID


class student_response(Entity_Response):
    deleted: bool
    note: Optional[Dict | str] = {}
    user_pk_id: UUID
    emergency_number: Optional[int | str]
    # create_date: str
    created_fk_by: UUID
    nickname: Optional[str]

    class Config:
        extra = 'ignore'
        orm_mode = True
