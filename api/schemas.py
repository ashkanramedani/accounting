from datetime import datetime, date, time, timedelta
from enum import Enum
from typing import Optional, List, Any
from uuid import UUID
from pydantic import BaseModel, PositiveInt


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


# -------------------   Authentications   -------------------
# class AuthenticationBase(BaseModel):
#     username: str
#     password: str
# class AuthenticationCreate(AuthenticationBase):
#     class Config:
#         orm_mode = True
# class Authentication(AuthenticationBase):
#     authentication_pk_id: int
#     class Config:
#         orm_mode = True
# class AuthenticationWithoutPassword(BaseModel):
#     username: str
#     authentication_pk_id: int
#     class Config:
#         orm_mode = True
# class AuthenticationLogin(BaseModel):
#     user_pk_id: Optional[int]
#     username: Optional[str]
#     mobile_number: Optional[str]
#     has_account: Optional[bool] = False
#     has_password: Optional[bool] = False
#     login_method: Optional[str]
#     otp_send_successful: Optional[bool]
#     email_send_successful: Optional[bool]

#     class Config:
#         orm_mode = True
# class Token(BaseModel):
#     user_pk_id: Optional[int]
#     refresh_token: Optional[str]
#     access_token: Optional[str]
#     type_token: Optional[str]
#     login_method: Optional[str]

#     class Config:
#         orm_mode = True

# -------------------------------   Users   -------------------------------
class UserBase(BaseModel):
    email: Optional[str]
    # fname: str
    # lname: str
    # mobile_number: str     
    # image: str    
    # employed: bool = True
    # panel_image: str | None = None
    # facebook_link: str | None = None
    # linkedin_link: str | None = None
    # twitter_link: str | None = None
    # instagram_link: str | None = None
    # telegram_link: str | None = None
    # whatsapp_link: str | None = None
    # self_introduction_video: str | None = None
    # department: str | None = None
    # teaching_start_date: datetime = None
    # teaching_languages: Dict = None
    # bio: str | None = None    
    # can_contact_to_me_from_site: bool = False    
    # about_me: Dict
    # meta_data: Dict = None   
    # nationality: Optional[str]
    # passport_id: Optional[str]
    # national_id: Optional[str]
    # address: Optional[str]
    # phone_number: Optional[str]
    # telegram_number: Optional[str]      
    # birth_date: Optional[str]
    # birth_place: Optional[str]
    # gender_fk_id: int = None
    # # branch_fk_id: int = None
    # priority: Optional[int] = None

    # departments_user: List = []
    # roles_user: List = []
    # posts_user: List = []   
    # products_user: List = []

    # authentication_fk_id = Column(BigInteger, ForeignKey("tbl_authentication.authentication_pk_id"))  
    # auth = relationship("Authentication", back_populates="auth_users")
    # courses_user = relationship('Course', secondary=courses_users_association, back_populates="users_course")
    # exams_user = relationship('Exam', secondary=exams_users_association, back_populates="users_exam")


class UserCreate(BaseModel):
    # branch_fk_id: int = 1
    # email: str
    # fname: str
    # lname: str
    # mobile_number: str
    # image: str
    # branch: str
    # gender: str
    # role_name: str
    # user_creator_fk_id: int

    class Config:
        orm_mode = True


class User(UserBase):
    user_pk_id: int

    # branch_fk_id: int
    # gender_fk_id: int 
    # authentication_fk_id: int = None

    class Config:
        orm_mode = True


class ProductUsers(BaseModel):
    fname: str
    lname: str
    user_pk_id: str
    image: str

    class Config:
        orm_mode = True


# class UserCreateAuth(BaseModel):
#     # password: str
#     fname: str
#     lname: str
#     mobile_number: str
#     email: str
#     class Config:
#         orm_mode = True
# class CandidateInfoForReport(BaseModel):
#     user_pk_id: int
#     mobile_number: str
#     email: str
#     image: str
#     fname: str
#     national_id: Optional[str] = ""
#     lname: str
#     class Config:
#         orm_mode = True

# -------------------   Posts   -------------------
class PostViwesBase(BaseModel):
    post_fk_id: int
    ip: str | None = None
    country: str | None = None
    user_creator_fk_id: int = None


class PostViwesCreate(PostViwesBase):
    class Config:
        orm_mode = True


class PostViwes(PostViwesBase):
    post_viwe_pk_id: int

    class Config:
        orm_mode = True


class UserInPost(BaseModel):
    user_pk_id: int
    fname: str
    lname: str
    image: str
    # gender: str
    deleted: bool

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    post_title: str
    post_summary: Optional[str] = ""
    post_discribtion: Optional[str] = ""
    post_content: Optional[str] = ""
    post_image: Optional[str] = "defult_post_image.jpg"
    priority: int = 5
    post_status: int = 0
    post_direction: Optional[str] = "RTL"
    post_type: str
    expire_date: Optional[date] = None

    # tags: List[TagsInPost] = None
    # users_post_speaker: List[UserInPost] = None
    # users_post_writer: List[UserInPost] = None
    # users_post_actor: List[UserInPost] = None
    # likes: List[LikesInPost] = None
    # comments: List[CommentsInPost] = None
    # views: List[ViwesInPost] = None


class PostCreate(PostBase):
    visible: bool = False
    category: Optional[List[str]] = []
    tag: Optional[List[str]] = []
    post_audio_file_link: Optional[str] = None
    post_audio_file_path: Optional[str] = None
    post_aparat_video_id: Optional[str] = None
    post_aparat_video_code: Optional[str] = None
    post_video_file_link: Optional[str] = None
    post_video_file_path: Optional[str] = None
    post_data_file_link: Optional[str] = None
    post_data_file_path: Optional[str] = None
    users_post_speaker: Optional[List[str]] = []
    users_post_writer: Optional[List[str]] = []
    users_post_actor: Optional[List[str]] = []
    user_creator_fk_id: Optional[int] = 1

    class Config:
        orm_mode = True


class PostUpdateData(BaseModel):
    class Config:
        orm_mode = True


class Post(PostBase):
    post_pk_id: int
    post_aparat_video_id: str | None = None
    post_aparat_video_code: str | None = None
    post_audio_file_link: str | None = None
    post_audio_file_path: str | None = None
    post_video_file_link: str | None = None
    post_video_file_path: str | None = None
    post_data_file_link: str | None = None
    post_data_file_path: str | None = None
    create_date: datetime

    class Config:
        orm_mode = True


class Posts(PostBase):
    create_date: datetime
    post_pk_id: int
    category: Optional[List[str]] = []
    tag: Optional[List[str]] = []
    users_post_speaker: Optional[List[str]] = []
    users_post_writer: Optional[List[str]] = []
    users_post_actor: Optional[List[str]] = []

    class Config:
        orm_mode = True


class PostStatus(BaseModel):
    post_pk_id: int
    post_status: int

    class Config:
        orm_mode = True


class PostDelete(BaseModel):
    post_pk_id: int

    class Config:
        orm_mode = True
        # users_post = relationship("Users", secondary=users_posts_association, backref="posts_user")

    # # post_category_id = Column(Integer, ForeignKey('tbl_categories.category_pk_id'))
    # # tags_post = relationship("Tag", secondary=tags_posts_association, backref="posts_tag")  
    # # comments = relationship("PostComments", backref="rel_comments")    
    # # list_views = relationship("PostViews", backref="rel_views")  
    # # likes = relationship("PostLikes", backref="rel_likes")   

    # educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True)
    # user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False)
    # user_delete_fk_id = Column(BigInteger, For


# -------------------------------   Tag  -------------------------------
class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    user_creator_tag_fk_id: int
    priority: Optional[int] = None

    class Config:
        orm_mode = True


class Tag(TagBase):
    tag_pk_id: UUID

    class Config:
        orm_mode = True


# -------------------   Categories  -------------------
class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    priority: Optional[int] = None

    class Config:
        orm_mode = True


class Category(CategoryBase):
    category_pk_id: UUID

    class Config:
        orm_mode = True


# -------------------   libraries   -------------------
class LibraryBase(BaseModel):
    library_name: str
    library_image: str = "book2.jpg"
    library_type: str = "public"
    library_description: Optional[str] = ""
    library_summer: Optional[str] = ""

    library_status: Optional[int] = 0

    library_audio_file_link: Optional[str] = None
    library_audio_file_path: Optional[str] = None
    library_aparat_video_id: Optional[str] = None
    library_aparat_video_code: Optional[str] = None
    library_video_file_link: Optional[str] = None
    library_video_file_path: Optional[str] = None
    library_data_file_link: Optional[str] = None
    library_data_file_path: Optional[str] = None

    priority: Optional[int] = None
    create_date: datetime


class LibraryCreate(LibraryBase):
    library_name: str
    library_image: str = "book2.jpg"
    library_type: str = "public"
    library_description: Optional[str] = ""
    library_summer: Optional[str] = ""

    library_audio_file_link: Optional[str] = None
    library_audio_file_path: Optional[str] = None
    library_aparat_video_id: Optional[str] = None
    library_aparat_video_code: Optional[str] = None
    library_video_file_link: Optional[str] = None
    library_video_file_path: Optional[str] = None
    library_data_file_link: Optional[str] = None
    library_data_file_path: Optional[str] = None

    class Config:
        orm_mode = True


class Library(LibraryBase):
    library_pk_id: int
    download_count: Optional[int] = 0

    class Config:
        orm_mode = True


class LibraryDelete(BaseModel):
    library_pk_id: int

    class Config:
        orm_mode = True


# --------------------------------------   Sahebkar   --------------------------------------

class Sort_Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Leave_type(str, Enum):
    vacation = "vacation"
    medical = "medical"


class job_title_Enum(str, Enum):
    teacher = "teacher"
    office = "office"
    rd = "rd"
    supervisor = "supervisor"


# --------------------------------------   Sahebkar   --------------------------------------
class Base_form(BaseModel):
    created_fk_by: UUID
    description: str | None = None
    status: int = 0


class StudentBase(BaseModel):
    description: str | None
    status: int = 0


class InstitutionsBase(BaseModel):
    created_fk_by: UUID


class Entity(BaseModel):
    name: str
    last_name: str
    day_of_birth: str | datetime = datetime.now()
    email: str | None
    mobile_number: str | None
    id_card_number: str | None
    address: str | None


# ========================== Entity ===========================
# ++++++++++++++++++++++++++ UserBase +++++++++++++++++++++++++++


class Role(Base_form):
    name: str
    cluster: str


class post_role_schema(Role):
    pass


class update_role_schema(Role):
    role_pk_id: UUID


class role_response(update_role_schema):
    role_pk_id: UUID
    name: str
    cluster: str

    class Config:
        orm_mode = True


class export_role(BaseModel):
    role_pk_id: UUID
    name: str
    cluster: str

    class Config:
        orm_mode = True


# ---------------------- Employee ----------------------

class Employee(Entity):
    priority: int | None
    fingerprint_scanner_user_id: int | None = None
    roles: List[UUID] | None = []


class post_employee_schema(Employee):
    pass


class update_employee_schema(Employee):
    employees_pk_id: UUID


class employee_response(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    roles: List[export_role] | None

    class Config:
        orm_mode = True


class export_employee(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    roles: List[export_role] | None

    class Config:
        orm_mode = True


# ---------------------- student ----------------------
class Student(Entity):
    level: str


class post_student_schema(Student):
    pass


class update_student_schema(Student):
    student_pk_id: UUID


class student_response(update_student_schema):
    pass

    class Config:
        orm_mode = True


class export_student(BaseModel):
    student_pk_id: UUID
    name: str
    last_name: str

    class Config:
        orm_mode = True


# +++++++++++++++++++++++ InstitutionsBase +++++++++++++++++++++++++++
# ---------------------- classes ----------------------
class classes(InstitutionsBase):
    name: str
    teachers: List[UUID] = []
    class_time: str | datetime = datetime.now()
    duration: PositiveInt


class post_class_schema(classes):
    pass


class update_class_schema(classes):
    class_pk_id: UUID


class classes_response(update_class_schema):
    class_pk_id: UUID

    class Config:
        orm_mode = True


class export_classes(BaseModel):
    class_pk_id: UUID
    name: str
    class_time: str | datetime = datetime.now()
    duration: PositiveInt | Any

    class Config:
        orm_mode = True


# ---------------------- question ----------------------
class Question(Base_form):
    text: str
    language: str


class post_questions_schema(Question):
    pass


class update_questions_schema(Question):
    question_pk_id: UUID


class Question_response(update_questions_schema):
    created: export_employee

    class Config:
        orm_mode = True


class export_question(BaseModel):
    question_pk_id: UUID
    text: str
    language: str

    class Config:
        orm_mode = True


# ======================== Forms =============================
# ++++++++++++++++++++++++++ EmployeeBase +++++++++++++++++++++++++++
# ---------------------- business_trip ----------------------
class business_trip(Base_form):
    employee_fk_id: UUID
    destination: str
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()


class post_business_trip_schema(business_trip):
    pass


class update_business_trip_schema(business_trip):
    business_trip_pk_id: UUID


class business_trip_response(update_business_trip_schema):
    business_trip_pk_id: UUID
    destination: str
    description: str
    created: export_employee
    employee: export_employee

    class Config:
        orm_mode = True


# ---------------------- leave_request ----------------------


class leave_request(Base_form):
    employee_fk_id: UUID
    leave_type: Leave_type = "vacation"
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now() + timedelta(days=1)


class post_leave_request_schema(leave_request):
    pass


class update_leave_request_schema(leave_request):
    leave_request_pk_id: UUID


class leave_request_response(update_leave_request_schema):
    created: export_employee
    employee: export_employee

    class Config:
        orm_mode = True


# ---------------------- remote_request ----------------------
class remote_request(Base_form):
    employee_fk_id: UUID
    start_date: str | datetime = datetime.now()
    end_date: str | datetime = datetime.now()
    working_location: str = ""


class post_remote_request_schema(remote_request):
    pass


class update_remote_request_schema(remote_request):
    remote_request_pk_id: UUID


class remote_request_response(update_remote_request_schema):
    created: export_employee
    employee: export_employee

    class Config:
        orm_mode = True


# ---------------------- fingerprint_scanner ----------------------


class fingerprint_scanner(Base_form):
    created_fk_by: UUID
    EnNo: int
    Name: str
    Date: date
    Enter: time
    Exit: time


class post_fingerprint_scanner_schema(fingerprint_scanner):
    pass


class update_fingerprint_scanner_schema(fingerprint_scanner):
    fingerprint_scanner_pk_id: UUID


class fingerprint_scanner_response(BaseModel):
    fingerprint_scanner_pk_id: UUID
    Date: date
    Enter: time
    Exit: time
    EnNo: int
    created: export_employee

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ TeacherBase +++++++++++++++++++++++++++
class class_cancellation(Base_form):
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement_date: str | datetime = datetime.now()
    class_duration: PositiveInt
    class_location: str


class post_class_cancellation_schema(class_cancellation):
    pass


class update_class_cancellation_schema(class_cancellation):
    class_cancellation_pk_id: UUID


class class_cancellation_response(update_class_cancellation_schema):
    created: export_employee
    teacher: export_employee
    classes: export_classes

    class Config:
        orm_mode = True


# ---------------------- teacher_tardy_reports ----------------------
class teacher_tardy_reports(Base_form):
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: PositiveInt


class post_teacher_tardy_reports_schema(teacher_tardy_reports):
    pass


class update_teacher_tardy_reports_schema(teacher_tardy_reports):
    teacher_tardy_reports_pk_id: UUID


class teacher_tardy_reports_response(update_teacher_tardy_reports_schema):
    created: export_employee
    teacher: export_employee
    classes: export_classes

    class Config:
        orm_mode = True


# ---------------------- teacher_replacement ----------------------

class teacher_replacement(Base_form):
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


class post_teacher_replacement_schema(teacher_replacement):
    pass


class update_teacher_replacement_schema(teacher_replacement):
    teacher_replacement_pk_id: UUID


class teacher_replacement_response(update_teacher_replacement_schema):
    created: export_employee
    main_teacher: export_employee
    replacement_teacher: export_employee
    classes: export_classes

    class Config:
        orm_mode = True


# ---------------------- payment_method ----------------------
class payment_method(Base_form):
    employee_fk_id: UUID
    shaba: str
    card_number: str


class post_payment_method_schema(payment_method):
    pass


class update_payment_method_schema(payment_method):
    payment_method_pk_id: UUID


class payment_method_response(update_payment_method_schema):
    created: export_employee
    employee: export_employee

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ Survey +++++++++++++++++++++++++++
# ---------------------- Survey_form ----------------------

class Survey(Base_form):
    questions: List[UUID]
    class_fk_id: UUID
    title: str


class post_survey_schema(Survey):
    pass


class update_survey_schema(Survey):
    survey_pk_id: UUID
    class_fk_id: UUID


class survey_response(update_survey_schema):
    created: export_employee
    classes: export_classes
    questions: List[export_question]

    class Config:
        orm_mode = True


class export_survey(BaseModel):
    survey_pk_id: UUID
    title: str

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ StudentBase +++++++++++++++++++++++++++
# ---------------------- response ----------------------
class Response(StudentBase):
    student_fk_id: UUID
    question_fk_id: UUID
    survey_fk_id: UUID
    answer: str


class post_response_schema(Response):
    pass


class update_response_schema(Response):
    response_pk_id: UUID


class response_response(update_response_schema):
    student: export_student
    question: export_question
    survey: export_survey

    class Config:
        orm_mode = True


# ---------------------- Salary ----------------------
class SalaryPolicy(BaseModel):
    created_fk_by: UUID
    employee_fk_id: UUID

    day_starting_time: Optional[time] = None
    day_ending_time: Optional[time] = None

    # finger_print
    Regular_hours_factor: float
    Regular_hours_cap: Optional[int] = None

    overtime_permission: bool
    overtime_factor: float
    overtime_cap: int
    overtime_threshold: int

    undertime_factor: float
    undertime_threshold: int

    # off_Day
    off_day_permission: bool
    off_day_factor: float
    off_day_cap: int

    # Remote
    remote_permission: bool
    remote_factor: float
    remote_cap: int

    # Leave_form
    medical_leave_factor: float
    medical_leave_cap: int

    vacation_leave_factor: float
    vacation_leave_cap: int

    # business_Trip
    business_trip_permission: bool
    business_trip_factor: float
    business_trip_cap: int


class post_SalaryPolicy_schema(SalaryPolicy):
    pass


class update_SalaryPolicy_schema(SalaryPolicy):
    salary_pk_id: UUID


class SalaryPolicy_response(update_SalaryPolicy_schema):
    created: export_employee
    employee: export_employee

    class Config:
        orm_mode = True


# ++++++++++++++++++++++++++ Reports +++++++++++++++++++++++++++
class salary_report(BaseModel):
    employee_fk_id: UUID
    year: PositiveInt
    month: PositiveInt

class teacher_report(BaseModel):
    teacher_fk_id: UUID
    start_date: Any
    end_date: Any

class employee_report(BaseModel):
    employee_fk_id: UUID
    start_date: datetime
    end_date: datetime

