from ..Base import *

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
