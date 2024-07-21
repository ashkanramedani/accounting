import random
from uuid import uuid4

from ..Entity import *


# ---------------------- class ----------------------
class course(Base_form):
    course_name: str = f'Course_{uuid4().hex[0:8]}'

    starting_date: date = datetime.now().date()
    ending_date: date = (datetime.now() + timedelta(days=30)).date()
    course_capacity: int = random.randint(10, 30)

    course_language: UUID = "7f371975-e397-4fc5-b719-75e3978fc547"
    course_type: UUID = "7f485938-f59f-401f-8859-38f59f201f3e"

    course_code: str
    course_image: str = ""
    Course_price: float

    tags: Optional[List[Update_Relation]] = []
    categories: Optional[List[Update_Relation]] = []

    course_level: str = "Base"
    package_discount: float = 0


class post_course_schema(course):
    pass


class update_course_schema(course):
    course_pk_id: UUID


class Course_Calender(BaseModel):  # instant of session form (can be modify as needed)
    days_of_week: int
    session_date: date | str

    class Config:
        orm_mode = True


class course_response(Base_response):
    course_pk_id: UUID

    course_name: str
    package_discount: float
    course_image: str
    course_capacity: int
    course_level: str
    course_code: str

    starting_date: date
    ending_date: date

    teachers: List[export_employee | UUID] = None
    course_signature: List[Course_Calender] = []
    available_seat: int = None

    tags: List[export_tag] = []
    categories: List[export_categories] = []
    language: export_language
    type: export_course_type

    class Config:
        orm_mode = True
