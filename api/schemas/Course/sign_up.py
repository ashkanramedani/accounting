from schemas.Base import *


class post_pre_payment_sign_up(BaseModel):
    student_pk_id: UUID
    course_id: UUID
    sub_course_ids: List[UUID] = None
    discount_code: str = None


class active_course_response(BaseModel):
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
    session_signature: List = []
    available_seat: int = 0
    number_of_session: int = 0

    tags: List[export_tag] = []
    categories: List[export_categories] = []
    language: export_language
    type: export_course_type

    class Config:
        extra = 'ignore'
        orm_mode = True
