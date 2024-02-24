import datetime
import email
# from enum import unique
# from unicodedata import category
# from click import style
from typing import List, Union
from .database import Base
from sqlalchemy import Enum, Boolean, Column, ForeignKey, Integer, String, DateTime, Table, BigInteger, Date, Time, UniqueConstraint, Index, MetaData, Float, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import expression, func
from email.policy import default
from uuid import UUID
from typing import Optional, List, Dict, Any

from enum import Enum as PythonEnum
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


metadata_obj = MetaData()


from .database import Base

class BaseTable: 
    
    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expier_date = Column(DateTime(timezone=True), default=None)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    # user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False)

    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    # user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)    
    # user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

     

users_departments_association = Table(
    'rel_users_departments', 
    Base.metadata, 
    Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True),
    Column("department_fk_id", BigInteger, ForeignKey("tbl_departments.department_pk_id"), nullable=False, primary_key=True),
    Column("educational_institution_fk_id", BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=False, primary_key=True)
)

users_posts_actor_association = Table(
    'rel_users_posts_actor', 
    Base.metadata, 
    Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True),
    Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True)
)

users_posts_writer_association = Table(
    'rel_users_posts_writer', 
    Base.metadata, 
    Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True),
    Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True)
)

users_posts_speaker_association = Table(
    'rel_users_posts_speaker', 
    Base.metadata, 
    Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True),
    Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True)
)


class EducationalInstitutions(Base, BaseTable):
    __tablename__ = "tbl_educational_institutions"

    educational_institution_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
    educational_institution_name = Column(String(100), unique=True, nullable=False)
    educational_institution_hash = Column(String(100), unique=True)

    def __repr__(self):
        return f'<EducationalInstitution "{self.educational_institution_pk_id}">'    

class Tags(Base):
    __tablename__ = "tbl_tags"

    tag_pk_id = Column(GUID, nullable=False, unique=True, primary_key=True, index=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    tag_name = Column(String(100), unique=True, nullable=False)
    
    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expier_date = Column(DateTime(timezone=True), default=None)
    
    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)    
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    def __repr__(self):
        return f'<Tag "{self.tag_pk_id}">'

class Categories(Base):
    __tablename__ = "tbl_categories"

    category_pk_id = Column(GUID, nullable=False, unique=True, primary_key=True, index=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)  
    category_name = Column(String(100), index=True, nullable=False)    
    
    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expier_date = Column(DateTime(timezone=True), default=None)
    
    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)    
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    def __repr__(self):
        return f'<Category "{self.category_pk_id}">' 

# class Authentications(Base, BaseTable):
#     __tablename__ = "tbl_authentications"
#     authentication_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
#     username = Column(String, index=True, unique=True, nullable=False)
#     password = Column(String, nullable=False)  
#     auth_users = relationship("Users", back_populates="auth") 

#     def __repr__(self):
#         return f'<Authentication "{self.username}">' 

class Users(Base, BaseTable):
    __tablename__ = "tbl_users"

    user_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)

    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)   
    email = Column(String(50), nullable=False, index=True)
    mobile_number = Column(String(15), server_default='', nullable=False)    
    image = Column(String(50), server_default='male.jpg', nullable=False)
    employed = Column(Boolean, server_default=expression.false(), nullable=False)
    # panel_image = Column(String(50), server_default='male.jpg', nullable=False)   
    # nationality = Column(String(50), server_default='iranian', nullable=False) 
    # passport_id = Column(String(20), default=None)    
    # national_id = Column(String(20), default=None)
    # can_contact_to_me_from_site = Column(Boolean, server_default=expression.false(), nullable=False)    
    # self_introduction_video = Column(String(250), server_default='', nullable=False)
    # address = Column(String(5000), default=None)
    # phone_number = Column(String(15), default=None)
    # telegram_number = Column(String(15), default=None)  
    # bio = Column(String(5000), default=None)    
    # facebook_link = Column(String(250), default=None)
    # linkedin_link = Column(String(250), default=None)
    # twitter_link = Column(String(250), default=None)
    # instagram_link = Column(String(250), default=None)
    # telegram_link = Column(String(250), default=None)
    # whatsapp_link = Column(String(250), default=None)
    
    # birth_date = Column(DateTime(timezone=True), default=None)
    # birth_place = Column(String(250), default=None)  

    # departments_user = relationship('Departments', secondary=users_departments_association, back_populates="users_department")
    # users_roles = relationship("UserRole", back_populates="user")
    # posts_user_speaker = relationship("Posts", secondary=users_posts_speaker_association, back_populates="users_post_speaker")    
    # posts_user_writer = relationship("Posts", secondary=users_posts_writer_association, back_populates="users_post_writer")    
    # posts_user_actor = relationship("Posts", secondary=users_posts_actor_association, back_populates="users_post_actor")    
    # # products_user = relationship('Products', secondary=products_users_association, back_populates="users_product")
    # # user_courses_role = relationship('Courses', secondary=course_user_role_association, back_populates="course_users_roles")

    # auth = relationship("Authentications", back_populates="auth_users")

    # gender_fk_id = Column(BigInteger, ForeignKey("tbl_genders.gender_pk_id"))
    # gender = relationship("Genders", back_populates="gender_user_list")

    # branch_fk_id = Column(BigInteger, ForeignKey("tbl_branches.branch_pk_id"))
    # branch = relationship("Branchs", back_populates="branch_user_list")
    
    # teaching_start_date = Column(DateTime(timezone=True), default=None)
    # teaching_languages = Column(JSONB, server_default='{}')
    # about_me = Column(JSONB, server_default='{}')
    # meta_data = Column(JSONB, server_default='{}')     
     
    # authentication_fk_id = Column(BigInteger, ForeignKey("tbl_authentications.authentication_pk_id"))  
    # courses_user = relationship('Course', secondary=courses_users_association, back_populates="users_course")
    # exams_user = relationship('Exam', secondary=exams_users_association, back_populates="users_exam")

    # educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True)
    # user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)
    # user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    # __table_args__ = (
    #     Index("idx_user_email_educational_institution_fk_id", email, educational_institution_fk_id, unique=True),
    #     UniqueConstraint(email, educational_institution_fk_id, name='u_user_email_educational_institution_fk_id'),
    # )

    def __repr__(self):
        return f'<User "{self.user_pk_id}">'    

class PostViwes(Base, BaseTable):    
    __tablename__ = "tbl_post_viwes"

    post_viwe_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
    post_fk_id = Column(BigInteger, ForeignKey("tbl_posts.post_pk_id"), nullable=False)
    ip = Column(String(250), default=None)
    country = Column(String(250), default=None)
    meta_data = Column(JSONB, server_default='{}')

    educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True)
    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    def __repr__(self):
        return f'<PostViwe "{self.post_viwe_pk_id}">'

class Posts(Base, BaseTable):
    __tablename__ = "tbl_posts"

    post_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
    post_title = Column(String)
    post_summary = Column(String)
    post_discribtion = Column(String)
    post_content = Column(String)
    post_image = Column(String) 
    post_type = Column(String, index=True)
    post_audio_file_link = Column(String)
    post_audio_file_path = Column(String)  
    post_aparat_video_id = Column(String)
    post_aparat_video_code = Column(String)    
    post_video_file_link = Column(String)
    post_video_file_path = Column(String)  
    post_data_file_link = Column(String)
    post_data_file_path = Column(String)
    post_direction = Column(String)
    post_status = Column(Integer,  default=5, nullable=False) 

    # users_post_speaker = relationship("Users", secondary=users_posts_speaker_association, back_populates="posts_user_speaker")  
    # users_post_writer = relationship("Users", secondary=users_posts_writer_association, back_populates="posts_user_writer")  
    # users_post_actor = relationship("Users", secondary=users_posts_actor_association, back_populates="posts_user_actor")  
    # post_viwe = relationship("Users", secondary=users_posts_writer_association, back_populates="posts_user_writer")  

    # post_category_id = Column(Integer, ForeignKey('tbl_categories.category_pk_id'))
    # tags_post = relationship("Tag", secondary=tags_posts_association, backref="posts_tag")  
    # comments = relationship("PostComments", backref="rel_comments")    
    # list_views = relationship("PostViews", backref="rel_views")  
    # likes = relationship("PostLikes", backref="rel_likes")   

    educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True)
    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False)
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    def __repr__(self):
        return f'<Post "{self.post_pk_id}">'

class Libraries(Base):
    __tablename__ = "tbl_libraries"

    library_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)

    library_name = Column(String, nullable=False)     
    library_image = Column(String, default="book2.jpg", nullable=False)
    library_type = Column(String, default="educational_products", nullable=False)
    library_description = Column(String)
    library_summer = Column(String)

    library_audio_file_link = Column(String)
    library_audio_file_path = Column(String) 

    library_aparat_video_id = Column(String)
    library_aparat_video_code = Column(String)  

    library_video_file_link = Column(String)
    library_video_file_path = Column(String)

    library_data_file_link = Column(String)
    library_data_file_path = Column(String) 

    library_download_count = Column(Integer, default=0, nullable=False) 

    educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True) 
    
    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expier_date = Column(DateTime(timezone=True), default=None)
    
    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)    
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    def __repr__(self):
        return f'<Library "{self.library_pk_id}">'



IDs = {
    "employees": "employees.employees_pk_id",
    "classes": "classes.class_pk_id",
    "days": "days.day_pk_id",
    "survey_form": "survey_form.form_pk_id",
    "question": "question.question_pk_id",
    "student": "student.student_pk_id",
    "payment_method": "payment_method.payment_method_pk_id"
}

class WeekdayEnum(PythonEnum):
    MONDAY = "0"
    TUESDAY = "1"
    WEDNESDAY = "2"
    THURSDAY = "3"
    FRIDAY = "4"
    SATURDAY = "5"
    SUNDAY = "6"

class fingerprint_scanner_Mode(PythonEnum):
    Normal = "Normal"

class job_title_Enum(PythonEnum):
    teacher = "teacher"
    office = "office"
    RandD = "R&D"
    Supervisor = "Supervisor"


def create_Unique_ID():
    return Column(GUID,
                  server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
                  primary_key=True,
                  nullable=False,
                  unique=True,
                  index=True)

def create_forenKey(table: str, nullable=False):
    return Column(GUID,
                  ForeignKey(IDs[table], ondelete='SET NULL'), nullable=nullable)


class BaseTable:
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    priority = Column(Integer, default=5, nullable=True)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    delete_date = Column(DateTime(timezone=True), default=None)
    expire_date = Column(DateTime(timezone=True), default=None)

class Leave_request_form(Base, BaseTable):
    __tablename__ = "leave_request"
    leave_request_pk_id = create_Unique_ID()
    created_for_fk_id = create_forenKey("employees")
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    Description = Column(String)

class Student_form(Base, BaseTable):
    __tablename__ = "student"
    student_pk_id = create_Unique_ID()
    student_name = Column(String, nullable=False)
    student_last_name = Column(String, index=True)
    student_level = Column(String, index=True)
    student_age = Column(Integer)

class Class_form(Base, BaseTable):
    __tablename__ = "classes"
    class_pk_id = create_Unique_ID()
    starting_time = Column(Time, nullable=False)
    duration = Column(Interval)
    class_date = Column(DateTime, nullable=False)

class Employees_form(Base, BaseTable):
    __tablename__ = "employees"
    employees_pk_id = create_Unique_ID()
    name = Column(String, nullable=False)
    last_name = Column(String, index=True)
    job_title = Column(Enum(job_title_Enum), index=True)
    fingerprint_scanner_user_id = Column(String, nullable=True, default="Not Specified")

class Remote_Request_form(Base, BaseTable):
    __tablename__ = "remote_requests"
    remote_request_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    create_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    working_location = Column(String)
    description = Column(String)

class Teacher_tardy_reports_form(Base, BaseTable):
    __tablename__ = "teacher_tardy_reports"
    teacher_tardy_reports_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    delay = Column(Interval)

class Class_Cancellation_form(Base, BaseTable):
    __tablename__ = "class_cancellation"
    class_cancellation_pk_id = create_Unique_ID()
    created_date = Column(Date)
    created_fk_by = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    teacher_fk_id = create_forenKey("employees")
    replacement = Column(Date)
    class_duration = Column(Interval)
    class_location = Column(String)
    description = Column(String)

class Teacher_Replacement_form(Base, BaseTable):
    __tablename__ = "teacher_replacement"
    teacher_replacement_pk_id = create_Unique_ID()
    created_by_fk_id = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    replacement_teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")

class Business_Trip_form(Base, BaseTable):
    __tablename__ = "business_trip"
    business_trip_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    destination = Column(String)
    description = Column(String)

class Teachers_Report_form(Base, BaseTable):
    __tablename__ = "teachers_report"
    teachers_report_pk_id = create_Unique_ID()
    created_by_fk_id = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    score = Column(Float)
    number_of_student = Column(Integer)
    canceled_classes = Column(Integer, default=0)
    replaced_classes = Column(Integer, default=0)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)


## Survey Form
class survey_form(Base, BaseTable):
    __tablename__ = "survey_form"

    form_pk_id = create_Unique_ID()
    class_fk_id = create_forenKey("classes")
    title = Column(String, index=True)

class Questions_form(Base, BaseTable):
    __tablename__ = "question"
    question_pk_id = create_Unique_ID()
    text = Column(String, unique=True)

class survey_questions_form(Base, BaseTable):
    __tablename__ = 'survey_form_questions'
    survey_questions = create_Unique_ID()
    form_fk_id = create_forenKey("survey_form")
    question_fk_id = create_forenKey("question")

class response_form(Base, BaseTable):
    __tablename__ = "response"
    response_pk_id = create_Unique_ID()
    student_fk_id = create_forenKey("student")
    question_fk_id = create_forenKey("question")
    form_fk_id = create_forenKey("survey_form")
    answer = Column(String)

class payment_method_form(Base, BaseTable):
    __tablename__ = "payment_method"
    payment_method_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    shaba = Column(String, nullable=False, unique=True)
    card_number = Column(String, nullable=True, unique=True)
    active = Column(Boolean, default=False)

class fingerprint_scanner_form(Base):
    __tablename__ = "fingerprint_scanner"
    fingerprint_scanner_pk_id = create_Unique_ID()
    user_ID = Column(String, nullable=False)
    In_Out = Column(Enum(fingerprint_scanner_Mode), nullable=True)
    Antipass = Column(Integer, default=0)
    ProxyWork = Column(Integer, default=0)
    DateTime = Column(DateTime)
