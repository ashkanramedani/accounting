import pstats
from fastapi import Query, Body
from datetime import datetime, time, timedelta, date
from typing import List, Union, Optional, Dict
from datetime import datetime, time, timedelta, date
from enum import Enum
from uuid import UUID
from typing import Optional, List, Dict, Any

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

from pydantic import BaseModel


class WeekdayEnum(str, Enum):
    MONDAY = "0"
    TUESDAY = "1"
    WEDNESDAY = "2"
    THURSDAY = "3"
    FRIDAY = "4"
    SATURDAY = "5"
    SUNDAY = "6"


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
    # panel_image: str = None
    # facebook_link: str = None
    # linkedin_link: str = None
    # twitter_link: str = None
    # instagram_link: str = None
    # telegram_link: str = None
    # whatsapp_link: str = None
    # self_introduction_video: str = None
    # department: str = None
    # teaching_start_date: datetime = None
    # teaching_languages: Dict = None
    # bio: str = None    
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
    ip: str = None
    country: str = None
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
    expier_date: Optional[date] = None

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
    post_aparat_video_id: str = None
    post_aparat_video_code: str = None
    post_audio_file_link: str = None
    post_audio_file_path: str = None
    post_video_file_link: str = None
    post_video_file_path: str = None
    post_data_file_link: str = None
    post_data_file_path: str = None
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

    library_audio_file_link: Optional[str] = None
    library_audio_file_path: Optional[str] = None
    library_aparat_video_id: Optional[str] = None
    library_aparat_video_code: Optional[str] = None
    library_video_file_link: Optional[str] = None
    library_video_file_path: Optional[str] = None
    library_data_file_link: Optional[str] = None
    library_data_file_path: Optional[str] = None

    priority: Optional[int] = None


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


# --------------------------------------   Sahebkar   --------------------------------------
class fingerprint_scanner_Mode(str, Enum):
    Normal = "Normal"


class job_title_Enum(str, Enum):
    teacher = "teacher"
    office = "office"
    RandD = "R&D"
    Supervisor = "Supervisor"


class post_employee_schema(BaseModel):
    name: str
    last_name: str
    job_title: job_title_Enum
    priority: int | None
    user_ID: str | None


class update_employee_schema(BaseModel):
    employees_pk_id: UUID
    name: str
    last_name: str
    job_title: job_title_Enum
    priority: int | None
    user_ID: str | None


class post_leave_request_schema(BaseModel):
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


class update_leave_request_schema(BaseModel):
    leave_request_id: UUID
    created_by: UUID
    created_for: UUID
    start_date: datetime
    end_date: datetime
    Description: str


class post_student_schema(BaseModel):
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


class update_student_schema(BaseModel):
    student_pk_id: UUID
    student_name: str
    student_last_name: str
    student_level: str
    student_age: int


class post_class_schema(BaseModel):
    starting_time: time
    duration: int
    class_date: date


class update_class_schema(BaseModel):
    class_pk_id: UUID
    starting_time: time
    duration: int
    class_date: date


class post_remote_request_schema(BaseModel):
    employee_fk_id: UUID
    start_date: date
    end_date: date
    working_location: str
    description: str


class update_remote_request_schema(BaseModel):
    remote_request_pk_id: UUID
    employee_fk_id: UUID
    start_date: date
    end_date: date
    working_location: str
    description: str


class post_teacher_tardy_reports_schema(BaseModel):
    create_by_fk_id: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


class update_teacher_tardy_reports_schema(BaseModel):
    teacher_tardy_reports_pk_id: UUID
    create_by_fk_id: UUID
    teacher_fk_id: UUID
    class_fk_id: UUID
    delay: timedelta


class post_class_cancellation_schema(BaseModel):
    create_by_fk_id: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


class update_class_cancellation_schema(BaseModel):
    class_cancellation_pk_id: UUID
    create_by_fk_id: UUID
    class_fk_id: UUID
    teacher_fk_id: UUID
    replacement: date
    class_duration: timedelta
    class_location: str
    description: str


class post_teacher_replacement_schema(BaseModel):
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


class update_teacher_replacement_schema(BaseModel):
    teacher_replacement_pk_id: UUID
    created_by_fk_id: UUID
    teacher_fk_id: UUID
    replacement_teacher_fk_id: UUID
    class_fk_id: UUID


class post_business_trip_schema(BaseModel):
    employee_fk_id: UUID
    destination: str
    description: str


class update_business_trip_schema(BaseModel):
    business_trip_pk_id: UUID
    employee_fk_id: UUID
    destination: str
    description: str


class post_day_schema(BaseModel):
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta


class update_day_schema(BaseModel):
    day_pk_id: UUID
    date: date
    day_of_week: WeekdayEnum
    entry_time: date
    exit_time: date
    duration: timedelta


class post_questions_schema(BaseModel):
    text: str


class update_questions_schema(BaseModel):
    question_pk_id: UUID
    text: str


class post_survey_schema(BaseModel):
    class_fk_id: UUID
    questions: List[UUID]
    title: str


class update_survey_schema(BaseModel):
    form_pk_id: UUID
    class_fk_id: UUID
    questions: List[UUID]
    title: str


class post_response_schema(BaseModel):
    student_fk_id: UUID
    question_fk_id: UUID
    form_fk_id: UUID
    answer: str


class update_response_schema(BaseModel):
    response_pk_id: UUID
    student_fk_id: UUID
    question_fk_id: UUID
    form_fk_id: UUID
    answer: str


class post_class_form_schema(BaseModel):
    starting_time: date
    duration: timedelta
    class_date: datetime


class update_class_form_schema(BaseModel):
    class_pk_id: UUID
    starting_time: date
    duration: timedelta
    class_date: datetime


class post_payment_method_schema(BaseModel):
    employee_fk_id: UUID
    shaba: str
    card_number: str


class update_payment_method_schema(BaseModel):
    payment_method_pk_id: UUID
    employee_fk_id: UUID
    shaba: str
    card_number: str


class post_fingerprint_scanner_schema(BaseModel):
    created_by_fk_id: UUID
    In_Out: fingerprint_scanner_Mode
    Antipass: bool
    ProxyWork: bool
    DateTime: datetime
    user_ID: str


class FingerPrint_Record(BaseModel):
    user_ID: str
    In_Out: str
    Antipass: str
    ProxyWork: str
    DateTime: str


class post_bulk_fingerprint_scanner_schema(BaseModel):
    created_by_fk_id: UUID
    Records: List[FingerPrint_Record]


class update_fingerprint_scanner_schema(BaseModel):
    fingerprint_scanner_pk_id: UUID
    employee_fk_id: UUID
    created_by_fk_id: UUID
    In_Out: fingerprint_scanner_Mode
    Antipass: str
    ProxyWork: str
    DateTime: datetime
