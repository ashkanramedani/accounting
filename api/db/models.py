# from enum import unique
# from unicodedata import category
# from click import style
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, BigInteger, MetaData, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression, func

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


###### TMP @@@@@@@
class Department(Base):
    __tablename__ = 'tbl_departments'
    department_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)


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

    # class Authentications(Base, Base_form):


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
    post_status = Column(Integer, default=5, nullable=False)

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


# functions

IDs = {
    "employees": "employees.employees_pk_id",
    "classes": "classes.class_pk_id",
    "days": "days.day_pk_id",
    "survey": "survey.survey_pk_id",
    "question": "question.question_pk_id",
    "student": "student.student_pk_id",
    "payment_method": "payment_method.payment_method_pk_id"
}


def create_Unique_ID():
    return Column(GUID,
                  server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
                  primary_key=True,
                  nullable=False,
                  unique=True,
                  index=True)


def create_forenKey(table: str):
    return Column(GUID, ForeignKey(IDs[table]), nullable=False)


# Base
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


class InstitutionsBase(BaseTable):
    pass


class Base_form(BaseTable):
    description = Column(String, nullable=True, default="")
    status = Column(Integer, nullable=False, default=0)


class UserBase(BaseTable):
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    day_of_birth = Column(DateTime, nullable=True)
    email = Column(String(50), nullable=True, index=True)
    mobile_number = Column(String, server_default='', nullable=False)
    id_card_number = Column(String, nullable=True)
    address = Column(String(5000), default=None)


# ========================== Entity ===========================

# ++++++++++++++++++++++++++ UserBase +++++++++++++++++++++++++++
class Employees_form(Base, UserBase):
    __tablename__ = "employees"
    employees_pk_id = create_Unique_ID()
    job_title = Column(String, nullable=False)
    fingerprint_scanner_user_id = Column(String, nullable=False, default="Not Specified")

    Survey_Relation = relationship("Survey_form", back_populates="created", foreign_keys="Survey_form.created_fk_by")
    Questions_Relation = relationship("Questions_form", back_populates="created", foreign_keys="Questions_form.created_fk_by")
    Business_Trip_Relation = relationship("Business_Trip_form", back_populates="created", foreign_keys="Business_Trip_form.created_fk_by")
    Leave_request_Relation = relationship("Leave_request_form", back_populates="created", foreign_keys="Leave_request_form.created_fk_by")
    Remote_Request_Relation = relationship("Remote_Request_form", back_populates="created", foreign_keys="Remote_Request_form.created_fk_by")
    payment_method_Relation = relationship("Payment_method_form", back_populates="created", foreign_keys="Payment_method_form.created_fk_by")
    Class_Cancellation_Relation = relationship("Class_Cancellation_form", back_populates="created", foreign_keys="Class_Cancellation_form.created_fk_by")
    Teacher_Replacement_Relation = relationship("Teacher_Replacement_form", back_populates="created", foreign_keys="Teacher_Replacement_form.created_fk_by")
    Teacher_tardy_reports_Relation = relationship("Teacher_tardy_reports_form", back_populates="created", foreign_keys="Teacher_tardy_reports_form.created_fk_by")


class Student_form(Base, UserBase):
    __tablename__ = "student"
    student_pk_id = create_Unique_ID()
    level = Column(String, index=True)

    student_Relation = relationship("Response_form", back_populates="student", foreign_keys="Response_form.student_fk_id")


# +++++++++++++++++++++++ InstitutionsBase +++++++++++++++++++++++++++
class Class_form(Base, InstitutionsBase):
    __tablename__ = "classes"
    class_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    name = Column(String)
    class_time = Column(DateTime, nullable=False)
    duration = Column(Integer)


# ======================== Forms =============================

# ++++++++++++++++++++++++++ EmployeeBase +++++++++++++++++++++++++++

class Leave_request_form(Base, Base_form):
    __tablename__ = "leave_request"
    leave_request_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    employee_fk_id = create_forenKey("employees")
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    description = Column(String)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Leave_request_Relation")
    employee = relationship("Employees_form", foreign_keys=[employee_fk_id])


class Business_Trip_form(Base, Base_form):
    __tablename__ = "business_trip"
    business_trip_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    created_fk_by = create_forenKey("employees")
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    destination = Column(String)
    description = Column(String)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Business_Trip_Relation")
    employee = relationship("Employees_form", foreign_keys=[employee_fk_id])


class Remote_Request_form(Base, Base_form):
    __tablename__ = "remote_requests"
    remote_request_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    created_fk_by = create_forenKey("employees")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    working_location = Column(String, nullable=False)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Remote_Request_Relation")
    employee = relationship("Employees_form", foreign_keys=[employee_fk_id])


class Payment_method_form(Base, Base_form):
    __tablename__ = "payment_method"
    payment_method_pk_id = create_Unique_ID()
    employee_fk_id = create_forenKey("employees")
    created_fk_by = create_forenKey("employees")
    shaba = Column(String, nullable=False)
    card_number = Column(String, nullable=True)
    active = Column(Boolean, default=False)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="payment_method_Relation")
    employee = relationship("Employees_form", foreign_keys=[employee_fk_id])


class fingerprint_scanner_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner"
    fingerprint_scanner_pk_id = create_Unique_ID()
    user_ID = Column(String, nullable=False)
    In_Out = Column(String, nullable=True)
    Antipass = Column(Integer, default=0)
    ProxyWork = Column(Integer, default=0)
    DateTime = Column(DateTime)


# ++++++++++++++++++++++++++ TeacherBase +++++++++++++++++++++++++++

class Teacher_tardy_reports_form(Base, Base_form):
    __tablename__ = "teacher_tardy_reports"
    teacher_tardy_reports_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    delay = Column(Integer, nullable=False)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Teacher_tardy_reports_Relation")
    teacher = relationship("Employees_form", foreign_keys=[teacher_fk_id])
    classes = relationship("Class_form", foreign_keys=[class_fk_id])


class Class_Cancellation_form(Base, Base_form):
    __tablename__ = "class_cancellation"
    class_cancellation_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    class_duration = Column(Integer, nullable=False)
    class_location = Column(String, nullable=False)

    replacement_date = Column(DateTime, nullable=False)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Class_Cancellation_Relation")
    teacher = relationship("Employees_form", foreign_keys=[teacher_fk_id])
    classes = relationship("Class_form", foreign_keys=[class_fk_id])


class Teacher_Replacement_form(Base, Base_form):
    __tablename__ = "teacher_replacement"
    teacher_replacement_pk_id = create_Unique_ID()
    replacement_teacher_fk_id = create_forenKey("employees")
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Teacher_Replacement_Relation")
    main_teacher = relationship("Employees_form", foreign_keys=[teacher_fk_id])
    replacement_teacher = relationship("Employees_form", foreign_keys=[replacement_teacher_fk_id])
    classes = relationship("Class_form", foreign_keys=[class_fk_id])


class Teachers_Report_form(Base, Base_form):
    __tablename__ = "teachers_report"
    teachers_report_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    teacher_fk_id = create_forenKey("employees")
    class_fk_id = create_forenKey("classes")
    score = Column(Float)
    number_of_student = Column(Integer)
    canceled_classes = Column(Integer, default=0)
    replaced_classes = Column(Integer, default=0)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)


# ++++++++++++++++++++++++++ Survey +++++++++++++++++++++++++++

survey_questions = Table(
        "survey_questions",
        Base.metadata,
        Column("survey_fk_id", ForeignKey("survey.survey_pk_id")),
        Column("question_fk_id", ForeignKey("question.question_pk_id")))


class Survey_form(Base, Base_form):
    __tablename__ = "survey"
    survey_pk_id = create_Unique_ID()
    class_fk_id = create_forenKey("classes")
    created_fk_by = create_forenKey("employees")
    title = Column(String, index=True)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Survey_Relation")
    classes = relationship("Class_form", foreign_keys=[class_fk_id])
    questions = relationship('Questions_form', secondary=survey_questions, backref='surveys')


class Questions_form(Base, InstitutionsBase):
    __tablename__ = "question"
    question_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("employees")
    text = Column(String, unique=True)
    language = Column(String, index=True)

    created = relationship("Employees_form", foreign_keys=[created_fk_by], back_populates="Questions_Relation")


class Response_form(Base, Base_form):
    __tablename__ = "response"
    response_pk_id = create_Unique_ID()
    student_fk_id = create_forenKey("student")
    question_fk_id = create_forenKey("question")
    survey_fk_id = create_forenKey("survey")
    answer = Column(String, nullable=False)

    student = relationship("Student_form", foreign_keys=[student_fk_id], back_populates="student_Relation")
    question = relationship("Questions_form", foreign_keys=[question_fk_id])
    survey = relationship("Survey_form", foreign_keys=[survey_fk_id])
