from sqlalchemy import Boolean, Integer, String, DateTime, Table, BigInteger, Float, UniqueConstraint, DATE, TIME, Date, Time
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy.sql import expression, func

from .Func import *
from .database import Base

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

metadata_obj = MetaData()


class BaseTable:
    priority = Column(Integer, default=5, nullable=True)

    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    delete_date = Column(DateTime(timezone=True), default=None)
    expire_date = Column(DateTime(timezone=True), default=None)


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


# class Authentications(Base, Base_form):
#     __tablename__ = "tbl_authentications"
#     authentication_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
#     username = Column(String, index=True, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     auth_users = relationship("Users")
#
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

    # departments_user = relationship('Departments', secondary=users_departments_association)
    # users_roles = relationship("UserRole")
    # posts_user_speaker = relationship("Posts", secondary=users_posts_speaker_association)
    # posts_user_writer = relationship("Posts", secondary=users_posts_writer_association)
    # posts_user_actor = relationship("Posts", secondary=users_posts_actor_association)
    # # products_user = relationship('Products', secondary=products_users_association)
    # # user_classs_role = relationship('classs', secondary=class_user_role_association)

    # auth = relationship("Authentications")

    # gender_fk_id = Column(BigInteger, ForeignKey("tbl_genders.gender_pk_id"))
    # gender = relationship("Genders")

    # branch_fk_id = Column(BigInteger, ForeignKey("tbl_branches.branch_pk_id"))
    # branch = relationship("Branchs")

    # teaching_start_date = Column(DateTime(timezone=True), default=None)
    # teaching_languages = Column(JSONB, server_default='{}')
    # about_me = Column(JSONB, server_default='{}')
    # meta_data = Column(JSONB, server_default='{}')     

    # authentication_fk_id = Column(BigInteger, ForeignKey("tbl_authentications.authentication_pk_id"))  
    # classs_user = relationship('class', secondary=classs_users_association)
    # exams_user = relationship('Exam', secondary=exams_users_association)

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

    # users_post_speaker = relationship("Users", secondary=users_posts_speaker_association)
    # users_post_writer = relationship("Users", secondary=users_posts_writer_association)
    # users_post_actor = relationship("Users", secondary=users_posts_actor_association)
    # post_viwe = relationship("Users", secondary=users_posts_writer_association)

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

    library_status = Column(Integer, default=5, nullable=False)

    library_download_count = Column(Integer, default=0, nullable=False)

    educational_institution_fk_id = Column(BigInteger, ForeignKey("tbl_educational_institutions.educational_institution_pk_id"), nullable=True)

    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expire_date = Column(DateTime(timezone=True), default=None)

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


# Base
class BaseTable:
    priority = Column(Integer, default=5, nullable=True)

    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    delete_date = Column(DateTime(timezone=True), default=None)
    expire_date = Column(DateTime(timezone=True), default=None)


class Base_form(BaseTable):
    description = Column(String, nullable=True, default="")
    status = Column(Integer, nullable=False, default=0)
    # note = Column(JSON, nullable=True)


class InstitutionsBase(Base_form):
    pass


# +++++++++++++++++++++++ association +++++++++++++++++++++++++++
survey_questions = Table(
        "survey_questions",
        Base.metadata,
        Column("survey_fk_id", ForeignKey("survey.survey_pk_id")),
        Column("question_fk_id", ForeignKey("question.question_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("survey_fk_id", "question_fk_id", "deleted"), )

UserRole = Table(
        "users_roles",
        Base.metadata,
        Column("user_fk_id", ForeignKey("user.user_pk_id")),
        Column("role_fk_id", ForeignKey("role.role_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("user_fk_id", "role_fk_id", "deleted"), )

CourseTag = Table(
        "course_tag",
        Base.metadata,
        Column("tag_fk_id", ForeignKey("tag.tag_pk_id")),
        Column("course_fk_id", ForeignKey("course.course_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("tag_fk_id", "course_fk_id", "deleted"), )

CourseCategory = Table(
        "course_category",
        Base.metadata,
        Column("category_fk_id", ForeignKey("category.category_pk_id")),
        Column("course_fk_id", ForeignKey("course.course_pk_id")),
        Column("deleted", Boolean, default=False, nullable=False),
        UniqueConstraint("category_fk_id", "course_fk_id", "deleted"),
)


# ========================== Entity ===========================
# ++++++++++++++++++++++++++ UserBase +++++++++++++++++++++++++++
class User_form(Base, Base_form):
    __tablename__ = "user"
    user_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form", nullable=True)

    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    nickname = Column(String, index=True, nullable=True, default="")

    day_of_birth = Column(DateTime, nullable=True)
    email = Column(String(50), nullable=True, index=True)

    mobile_number = Column(String, default='', nullable=False)
    emergency_number = Column(String, default='', nullable=True)

    id_card_number = Column(String, nullable=True)
    address = Column(String(5000), default=None)

    fingerprint_scanner_user_id = Column(Integer, nullable=True)

    is_employee = Column(Boolean, default=True, nullable=False)
    level = Column(String, index=True, nullable=True)

    roles = relationship('Role_form', secondary=UserRole, backref='user_role')
    created = relationship("User_form", foreign_keys=[created_fk_by])

    __table_args__ = (UniqueConstraint('email', 'mobile_number', 'name', "last_name", "is_employee"),)


# +++++++++++++++++++++++ InstitutionsBase +++++++++++++++++++++++++++
class Course_form(Base, InstitutionsBase):
    __tablename__ = "course"
    course_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    course_language = create_forenKey("Language_form")
    course_type = create_forenKey("Course_Type_form")

    course_name = Column(String, unique=True)
    course_image = Column(String, nullable=True)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)
    course_capacity = Column(Integer, nullable=False)
    course_level = Column(String, nullable=False)
    course_code = Column(String, nullable=False)

    package_discount = Column(Float, nullable=False, default=0.0)

    tags = relationship("Tag_form", secondary=CourseTag, backref="course_tag")
    categories = relationship("Category_form", secondary=CourseCategory, backref="course_category")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    language = relationship("Language_form", foreign_keys=[course_language])
    type = relationship("Course_Type_form", foreign_keys=[course_type])

    __args__ = (UniqueConstraint('course_name', 'course_level', 'course_code'),)


class Sub_Course_form(Base, InstitutionsBase):
    __tablename__ = "sub_course"

    sub_course_pk_id = create_Unique_ID()
    course_fk_id = create_forenKey("Course_form")
    created_fk_by = create_forenKey("User_form")
    sub_course_teacher_fk_id = create_forenKey("User_form")

    sub_course_name = Column(String, unique=True)
    number_of_session = Column(Integer, nullable=False, default=0)
    sub_course_starting_date = Column(Date, nullable=False)
    sub_course_ending_date = Column(Date, nullable=False)

    sub_course_capacity = Column(Integer, nullable=False)
    sub_course_available_seat = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[sub_course_teacher_fk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])

    __args__ = (UniqueConstraint('sub_course_name', 'course_fk_id'),)


class Session_form(Base, InstitutionsBase):
    __tablename__ = "session"
    session_pk_id = create_Unique_ID()

    created_fk_by = create_forenKey("User_form")
    course_fk_id = create_forenKey("Course_form")
    sub_course_fk_id = create_forenKey("sub_course")
    session_teacher_fk_id = create_forenKey("User_form")
    sub_Request = create_forenKey("Sub_Request_form", nullable=True)

    is_sub = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)
    session_date = Column(Date, nullable=False)
    session_starting_time = Column(Time, nullable=False)
    session_ending_time = Column(Time, nullable=False)
    session_duration = Column(Integer, nullable=False)
    days_of_week = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    teacher = relationship("User_form", foreign_keys=[session_teacher_fk_id])


# ======================== Forms =============================
# ++++++++++++++++++++++++++ EmployeeBase +++++++++++++++++++++++++++

class Leave_Request_form(Base, Base_form):
    __tablename__ = "leave_request"
    leave_request_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    user_fk_id = create_forenKey("User_form")

    start_date = Column(TIME, index=True, nullable=True, default=None)
    end_date = Column(TIME, index=True, nullable=True, default=None)
    date = Column(DateTime, index=True)
    duration = Column(Integer, nullable=False, default=0)

    leave_type = Column(String, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    # __args__ = (UniqueConstraint('user_fk_id', 'start_date', 'end_date'),)


class Business_Trip_form(Base, Base_form):
    __tablename__ = "business_trip"
    business_trip_pk_id = create_Unique_ID()
    user_fk_id = create_forenKey("User_form")
    created_fk_by = create_forenKey("User_form")

    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    duration = Column(Integer, nullable=False, default=0)

    destination = Column(String, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    __args__ = (UniqueConstraint('user_fk_id', 'start_date', 'end_date'),)


class Remote_Request_form(Base, Base_form):
    __tablename__ = "remote_request"
    remote_request_pk_id = create_Unique_ID()
    user_fk_id = create_forenKey("User_form")
    created_fk_by = create_forenKey("User_form")
    working_location = Column(String, nullable=False)

    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])


class Payment_Method_form(Base, Base_form):
    __tablename__ = "payment_method"
    payment_method_pk_id = create_Unique_ID()
    user_fk_id = create_forenKey("User_form")
    created_fk_by = create_forenKey("User_form")
    shaba = Column(String(24), nullable=False)
    card_number = Column(String(16), nullable=True)
    active = Column(Boolean, default=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])


class Fingerprint_Scanner_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner"
    __table_args__ = (UniqueConstraint('EnNo', 'Date', 'Enter', 'Exit'),)

    fingerprint_scanner_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    EnNo = Column(Integer, nullable=False)
    Date = Column(DATE, nullable=False)
    Enter = Column(TIME, nullable=False)
    Exit = Column(TIME, nullable=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Fingerprint_Scanner_backup_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner_backup"
    __table_args__ = (UniqueConstraint('EnNo', 'DateTime'),)

    fingerprint_scanner_backup_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    TMNo = Column(Integer, nullable=False)
    EnNo = Column(Integer, nullable=False)
    GMNo = Column(Integer, nullable=False)
    Mode = Column(String)
    In_Out = Column(String)
    Antipass = Column(Integer)
    ProxyWork = Column(Integer)
    DateTime = Column(DateTime)

    created = relationship("User_form", foreign_keys=[created_fk_by])


# ++++++++++++++++++++++++++ TeacherBase +++++++++++++++++++++++++++

class Teacher_Tardy_report_form(Base, Base_form):
    __tablename__ = "teacher_tardy_report"
    teacher_tardy_report_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    teacher_fk_id = create_forenKey("User_form")
    course_fk_id = create_forenKey("Course_form")
    sub_course_fk_id = create_forenKey("Sub_Course_form")
    delay = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[teacher_fk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])


class Teachers_Report_form(Base, Base_form):
    __tablename__ = "teachers_report"
    teachers_report_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    teacher_fk_id = create_forenKey("User_form")
    course_fk_id = create_forenKey("Course_form")
    score = Column(Float)
    number_of_student = Column(Integer)
    canceled_course = Column(Integer, default=0)
    replaced_course = Column(Integer, default=0)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)


# ++++++++++++++++++++++++++ Survey +++++++++++++++++++++++++++

class Survey_form(Base, Base_form):
    __tablename__ = "survey"
    survey_pk_id = create_Unique_ID()
    sub_course_fk_id = create_forenKey("Sub_Course_form")
    created_fk_by = create_forenKey("User_form")
    title = Column(String, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    questions = relationship('Question_form', secondary=survey_questions, backref='surveys')


class Question_form(Base, InstitutionsBase):
    __tablename__ = "question"
    question_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    text = Column(String, unique=True)
    language = Column(String, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Response_form(Base, Base_form):
    __tablename__ = "response"
    response_pk_id = create_Unique_ID()
    user_fk_id = create_forenKey("User_form")
    question_fk_id = create_forenKey("Question_form")
    survey_fk_id = create_forenKey("Survey_form")
    answer = Column(String, nullable=False)

    student = relationship("User_form", foreign_keys=[user_fk_id])
    question = relationship("Question_form", foreign_keys=[question_fk_id])
    survey = relationship("Survey_form", foreign_keys=[survey_fk_id])


# Roles

class Role_form(Base, Base_form):
    __tablename__ = "role"

    role_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")

    name = Column(String, index=True, nullable=False, unique=True)
    cluster = Column(String, index=True, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])


# ++++++++++++++++++++++++++ Salary_Policy_form +++++++++++++++++++++++++++
class Salary_Policy_form(Base, Base_form):
    __tablename__ = "salary_policy"
    salary_policy_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    user_fk_id = create_forenKey("User_form", unique=True)

    Base_salary = Column(Float, nullable=False)
    Salary_Type = Column(String, nullable=False, default="Fixed")  # Fixed, Hourly, Split

    day_starting_time = Column(TIME, nullable=True, default=None)
    day_ending_time = Column(TIME, nullable=True, default=None)

    # finger_print
    Regular_hours_factor = Column(Float, nullable=False)
    Regular_hours_cap = Column(Integer, nullable=False)

    overtime_permission = Column(Boolean, nullable=False)
    overtime_factor = Column(Float, nullable=False)
    overtime_cap = Column(Integer, nullable=False)
    overtime_threshold = Column(Integer, nullable=False)

    undertime_factor = Column(Float, nullable=False)
    undertime_threshold = Column(Integer, nullable=False)

    # off day work
    off_day_permission = Column(Boolean, nullable=False)
    off_day_factor = Column(Float, nullable=False)
    off_day_cap = Column(Integer, nullable=False)

    # Remote
    remote_permission = Column(Boolean, nullable=False)
    remote_factor = Column(Float, nullable=False)
    remote_cap = Column(Integer, nullable=False)

    # Leave_form
    medical_leave_factor = Column(Float, nullable=False)
    medical_leave_cap = Column(Integer, nullable=False)

    vacation_leave_factor = Column(Float, nullable=False)
    vacation_leave_cap = Column(Integer, nullable=False)

    # business_Trip
    business_trip_permission = Column(Boolean, nullable=False)
    business_trip_factor = Column(Float, nullable=False)
    business_trip_cap = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def summery(self) -> dict:
        def Validate(key: str):
            for invalid_key in ["_fk_", "_pk_", "_sa_instance_"]:
                if invalid_key in key:
                    return False
            return True

        return {k: str(v) for k, v in self.__dict__.items() if Validate(k)}


class Employee_Salary_form(Base, Base_form):
    __tablename__ = "employee_salary"
    __table_args__ = (UniqueConstraint('user_fk_id', 'year', 'month'),)
    employee_salary_pk_id = create_Unique_ID()
    user_fk_id = create_forenKey("User_form")

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    fingerprint_scanner_user_id = Column(Integer, nullable=True)

    present_time = Column(Integer, nullable=False)
    regular_work_time = Column(Integer, nullable=False)
    overtime = Column(Integer, nullable=False)
    undertime = Column(Integer, nullable=False)
    off_Day_work_time = Column(Integer, nullable=False)

    Regular_earning = Column(Float, nullable=False)
    Overtime_earning = Column(Float, nullable=False)
    Undertime_earning = Column(Float, nullable=False)
    Off_Day_earning = Column(Float, nullable=False)

    remote = Column(Integer, nullable=False)
    remote_earning = Column(Float, nullable=False)
    vacation_leave = Column(Integer, nullable=False)
    vacation_leave_earning = Column(Integer, nullable=False)
    medical_leave = Column(Integer, nullable=False)
    medical_leave_earning = Column(Float, nullable=False)
    business_trip = Column(Integer, nullable=False)
    business_trip_earning = Column(Float, nullable=False)

    total_earning = Column(Float, nullable=False)
    Salary_Policy = Column(JSON, nullable=False)
    Days = Column(JSON, nullable=False)

    created = relationship("User_form", foreign_keys=[user_fk_id])


# ------------ Necessary for "Course" ------------
class Tag_form(Base, Base_form):
    __tablename__ = "tag"

    tag_pk_id = create_Unique_ID()
    tag_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Category_form(Base, Base_form):
    __tablename__ = "category"

    category_pk_id = create_Unique_ID()
    category_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Language_form(Base, Base_form):
    __tablename__ = "language"

    language_pk_id = create_Unique_ID()
    language_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Course_Type_form(Base, Base_form):
    __tablename__ = "course_type"

    course_type_pk_id = create_Unique_ID()
    course_type_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Status_form(Base, Base_form):  # NC: 002
    __tablename__ = "status"

    status_pk_id = create_Unique_ID()
    status_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])


class Sub_Request_form(Base, Base_form):
    __tablename__ = "sub_request"

    sub_request_pk_id = create_Unique_ID()
    created_fk_by = create_forenKey("User_form")
    session_fk_id = create_forenKey("Session_form")
    main_teacher_fk_id = create_forenKey("User_form")
    sub_teacher_fk_id = create_forenKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    sessions = relationship("Session_form", foreign_keys=[session_fk_id])
    main_teacher = relationship("User_form", foreign_keys=[main_teacher_fk_id])
    sub_teacher = relationship("User_form", foreign_keys=[sub_teacher_fk_id])


class Session_Cancellation_form(Base, Base_form):
    __tablename__ = "session_cancellation"

    session_cancellation_pk_id = create_Unique_ID()

    created_fk_by = create_forenKey("User_form")
    session_fk_id = create_forenKey("Session_form")

# class Reassign_Instructor_form(Base, Base_form):
#     __tablename__ = "reassign_instructor"
#
#     reassign_instructor_pk_id = create_Unique_ID()
#     created_fk_by = create_forenKey("User_form")
#     sessions_fk_id = create_forenKey("Session_form")
#     main_teacher_fk_id = create_forenKey("User_form")
#     sub_teacher_fk_id = create_forenKey("User_form")
#
#     created = relationship("User_form", foreign_keys=[created_fk_by])
#     sessions = relationship("Session_form", foreign_keys=[sessions_fk_id])
#     main_teacher = relationship("User_form", foreign_keys=[main_teacher_fk_id])
#     sub_teacher = relationship("User_form", foreign_keys=[sub_teacher_fk_id])
