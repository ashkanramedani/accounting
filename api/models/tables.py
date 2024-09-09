from typing import List

from sqlalchemy import Boolean, Integer, String, DateTime, Table, BigInteger, Float, UniqueConstraint, DATE, TIME, Date, Time, case
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import expression, func

from models.Func import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata_obj = MetaData()


class Base_form:
    priority = Column(Integer, default=5, nullable=True)

    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False, index=True)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    delete_date = Column(DateTime(timezone=True), default=None)
    expire_date = Column(DateTime(timezone=True), default=None)

    description = Column(String, nullable=True, default="")
    note = Column(JSON, nullable=True, default={})

    status = Column(String, nullable=False, default="submitted", index=True)  # NC: 006
    # status = Column(String, nullable=False, default="approved")  # NC: 006


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
        Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True, index=True),
        Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True, index=True)
)

users_posts_writer_association = Table(
        'rel_users_posts_writer',
        Base.metadata,
        Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True, index=True),
        Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True, index=True)
)

users_posts_speaker_association = Table(
        'rel_users_posts_speaker',
        Base.metadata,
        Column("user_fk_id", BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=False, primary_key=True, index=True),
        Column("post_fk_id", Integer, ForeignKey("tbl_posts.post_pk_id"), nullable=False, primary_key=True, index=True)
)


###### TMP @@@@@@@
class Department(Base):
    __tablename__ = 'tbl_departments'
    department_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)


class EducationalInstitutions(Base, Base_form):
    __tablename__ = "tbl_educational_institutions"

    educational_institution_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
    educational_institution_name = Column(String(100), unique=True, nullable=False)
    educational_institution_hash = Column(String(100), unique=True)

    def __repr__(self):
        return f'<EducationalInstitution "{self.educational_institution_pk_id}">'


#class Authentications(Base, Base_form):
#     __tablename__ = "tbl_authentications"
#     authentication_pk_id = Column(BigInteger, nullable=False, autoincrement=True, unique=True, primary_key=True, index=True)
#     username = Column(String, index=True, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     auth_users = relationship("Users")
#
#     def __repr__(self):
#         return f'<Authentication "{self.username}">'


class Users(Base, Base_form):
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


class PostViwes(Base, Base_form):
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


class Posts(Base, Base_form):
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

    user_creator_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)
    user_last_update_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)
    user_delete_fk_id = Column(BigInteger, ForeignKey("tbl_users.user_pk_id"), nullable=True)

    priority = Column(Integer, default=5, nullable=True)
    visible = Column(Boolean, server_default=expression.true(), nullable=False)
    expire_date = Column(DateTime(timezone=True), default=None)
    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    can_update = Column(Boolean, server_default=expression.true(), nullable=False)
    update_date = Column(DateTime(timezone=True), default=None, onupdate=func.now())
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)
    can_deleted = Column(Boolean, server_default=expression.true(), nullable=False)
    delete_date = Column(DateTime(timezone=True), default=None)

    def __repr__(self):
        return f'<Library "{self.library_pk_id}">'


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
    __table_args__ = (UniqueConstraint('email', 'mobile_number', 'name', "last_name", "is_employee"),)
    user_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form", nullable=True)

    name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    nickname = Column(String, index=True, nullable=True, default="")

    day_of_birth = Column(DateTime, nullable=True)
    email = Column(String(50), nullable=True, index=True)

    mobile_number = Column(String, default='', nullable=False)
    emergency_number = Column(String, default='', nullable=True)

    id_card_number = Column(String, nullable=True)
    address = Column(String(5000), default=None)

    fingerprint_scanner_user_id = Column(Integer, nullable=True, unique=True, default=None, index=True)

    is_employee = Column(Boolean, default=True, nullable=False, index=True)
    level = Column(String, index=True, nullable=True)
    ID_Experience = Column(Integer, default=0, nullable=False)  # total Working time from start

    roles = relationship('Role_form', secondary=UserRole, back_populates='users')

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


# +++++++++++++++++++++++ InstitutionsBase +++++++++++++++++++++++++++

class Course_form(Base, Base_form):
    __tablename__ = "course"
    __table_args__ = (UniqueConstraint('course_name', 'course_level', 'course_code'),)

    course_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    course_language = create_foreignKey("Language_form")
    course_type = create_foreignKey("Course_Type_form")

    course_name = Column(String)
    course_image = Column(String, nullable=True)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)
    course_capacity = Column(Integer, nullable=False)
    course_level = Column(String, nullable=False)
    course_code = Column(String, nullable=False)

    package_discount = Column(Float, nullable=False, default=0.0)
    Course_price = Column(Float, nullable=False)

    tags = relationship("Tag_form", secondary=CourseTag, backref="course_tag")
    categories = relationship("Category_form", secondary=CourseCategory, backref="course_category")

    created: Mapped["User_form"] = relationship("User_form", foreign_keys=[created_fk_by])
    language: Mapped["Language_form"] = relationship("Language_form", foreign_keys=[course_language])
    type: Mapped["Course_Type_form"] = relationship("Course_Type_form", foreign_keys=[course_type])
    sub_courses: Mapped[List["Sub_Course_form"]] = relationship("Sub_Course_form", back_populates='course')
    sessions: Mapped[List["Session_form"]] = relationship("Session_form", back_populates='course')

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Sub_Course_form(Base, Base_form):
    __tablename__ = "sub_course"
    __table_args__ = (UniqueConstraint('sub_course_name', 'course_fk_id'),)

    sub_course_pk_id = create_Unique_ID()
    course_fk_id = create_foreignKey("Course_form")
    created_fk_by = create_foreignKey("User_form")
    sub_course_teacher_fk_id = create_foreignKey("User_form")

    supervisor_review = Column(JSON, nullable=True)

    sub_course_name = Column(String, unique=True)
    number_of_session = Column(Integer, nullable=False, default=0)
    sub_course_starting_date = Column(Date, nullable=False)
    sub_course_ending_date = Column(Date, nullable=False)

    sub_request_threshold = Column(Integer, nullable=False, default=24)
    sub_course_capacity = Column(Integer, nullable=False)
    sub_course_available_seat = Column(Integer, nullable=False)
    sub_course_price = Column(Float, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[sub_course_teacher_fk_id])
    course: Mapped["Course_form"] = relationship("Course_form", foreign_keys=[course_fk_id], back_populates="sub_courses")
    sessions: Mapped[List["Session_form"]] = relationship("Session_form", back_populates="sub_course")

    # course = relationship("Course_form", foreign_keys=[course_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Session_form(Base, Base_form):
    __tablename__ = "session"
    __table_args__ = (UniqueConstraint('session_date', 'session_starting_time'),)

    session_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("sub_course")
    session_teacher_fk_id = create_foreignKey("User_form")
    sub_Request = create_foreignKey("Sub_Request_form", nullable=True)

    is_sub = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)
    session_date = Column(Date, nullable=False, index=True)
    session_starting_time = Column(Time, nullable=False, index=True)
    session_ending_time = Column(Time, nullable=False, index=True)
    session_duration = Column(Integer, nullable=False)
    days_of_week = Column(Integer, nullable=False)
    can_accept_sub = Column(DateTime, nullable=False, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher: Mapped["User_form"] = relationship("User_form", foreign_keys=[session_teacher_fk_id])
    course: Mapped["Course_form"] = relationship("Course_form", foreign_keys=[course_fk_id], back_populates="sessions")
    sub_course: Mapped["Sub_Course_form"] = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id], back_populates="sessions")

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


# ======================== Forms =============================
# ++++++++++++++++++++++++++ EmployeeBase +++++++++++++++++++++++++++

class Leave_Request_form(Base, Base_form):
    __tablename__ = "leave_request"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    leave_request_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")
    user_fk_id = create_foreignKey("User_form")

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    leave_type = Column(String, nullable=False)

    created: Mapped["User_form"] = relationship("User_form", foreign_keys=[created_fk_by])
    employee: Mapped["User_form"] = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Business_Trip_form(Base, Base_form):
    __tablename__ = "business_trip"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    business_trip_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    destination = Column(String, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Remote_Request_form(Base, Base_form):
    __tablename__ = "remote_request"
    __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    remote_request_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")

    working_location = Column(String, nullable=False)

    start = Column(TIME, index=True, nullable=True, default=None)
    end = Column(TIME, index=True, nullable=True, default=None)
    date = Column(Date, index=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Payment_Method_form(Base, Base_form):
    __tablename__ = "payment_method"
    __table_args__ = (UniqueConstraint('user_fk_id', 'shaba', 'card_number'),)

    payment_method_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")
    shaba = Column(String(24), nullable=False, unique=True)
    card_number = Column(String(16), nullable=True, unique=True)
    active = Column(Boolean, default=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Fingerprint_Scanner_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner"
    __table_args__ = (UniqueConstraint('EnNo', 'Date', 'Enter', 'Exit'),)

    fingerprint_scanner_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    EnNo = Column(Integer, nullable=False, index=True)
    Date = Column(DATE, nullable=False, index=True)
    Enter = Column(TIME, nullable=False, index=True)
    Exit = Column(TIME, nullable=True, index=True)
    duration = Column(Integer, nullable=False, default=0)

    created = relationship("User_form", foreign_keys=[created_fk_by])

    @hybrid_property
    def valid(self):
        return self.Enter is not None and self.Exit is not None

    @valid.expression
    def valid(self):
        return case(
                [(self.Enter.isnot(None) & self.Exit.isnot(None), True)],
                else_=False)

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Fingerprint_Scanner_backup_form(Base, Base_form):
    __tablename__ = "fingerprint_scanner_backup"
    __table_args__ = (UniqueConstraint('EnNo', 'DateTime'),)

    fingerprint_scanner_backup_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    TMNo = Column(Integer, nullable=False, index=True)
    EnNo = Column(Integer, nullable=False, index=True)
    GMNo = Column(Integer, nullable=False, index=True)
    Mode = Column(String)
    In_Out = Column(String)
    Antipass = Column(Integer)
    ProxyWork = Column(Integer)
    DateTime = Column(DateTime, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])

    # ++++++++++++++++++++++++++ TeacherBase +++++++++++++++++++++++++++

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teachers_Report_form(Base, Base_form):
    __tablename__ = "teachers_report"
    # __table_args__ = (UniqueConstraint('user_fk_id', 'start', 'end', 'date'),)

    teachers_report_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    teacher_fk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    score = Column(Float)
    number_of_student = Column(Integer)
    canceled_course = Column(Integer, default=0)
    replaced_course = Column(Integer, default=0)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    teacher_sheet_score = Column(Float, nullable=True)

    # ++++++++++++++++++++++++++ Survey +++++++++++++++++++++++++++

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Survey_form(Base, Base_form):
    __tablename__ = "survey"
    survey_pk_id = create_Unique_ID()
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    created_fk_by = create_foreignKey("User_form")
    title = Column(String, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    questions = relationship('Question_form', secondary=survey_questions, backref='surveys')

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Question_form(Base, Base_form):
    __tablename__ = "question"
    question_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")
    text = Column(String, unique=True)
    language = Column(String, index=True)

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Response_form(Base, Base_form):
    __tablename__ = "response"
    response_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    question_fk_id = create_foreignKey("Question_form")
    survey_fk_id = create_foreignKey("Survey_form")
    answer = Column(String, nullable=False)

    student = relationship("User_form", foreign_keys=[user_fk_id])
    question = relationship("Question_form", foreign_keys=[question_fk_id])
    survey = relationship("Survey_form", foreign_keys=[survey_fk_id])

    # Roles

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Role_form(Base, Base_form):
    __tablename__ = "role"

    role_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")

    name = Column(String, index=True, nullable=False, unique=True)
    cluster = Column(String, index=True, nullable=False)
    value = Column(Float, default=0.0)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    users = relationship('User_form', secondary=UserRole, back_populates='roles')

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)

    # ++++++++++++++++++++++++++ Salary_Policy_form +++++++++++++++++++++++++++


class Salary_Policy_form(Base, Base_form):
    __tablename__ = "salary_policy"
    salary_policy_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")
    user_fk_id = create_foreignKey("User_form")

    Base_salary = Column(Float, nullable=False)
    Fix_pay = Column(Float, nullable=False, default=0)
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

    employee = relationship("User_form", foreign_keys=[user_fk_id])
    created = relationship("User_form", foreign_keys=[created_fk_by])

    def summery(self) -> dict:
        def Validate(key: str):
            for invalid_key in ["_fk_", "_pk_", "_sa_instance_"]:
                if invalid_key in key:
                    return False
            return True

        return {k: str(v) for k, v in self.__dict__.items() if Validate(k)}

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Tag_form(Base, Base_form):
    __tablename__ = "tag"

    tag_pk_id = create_Unique_ID()
    tag_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Category_form(Base, Base_form):
    __tablename__ = "category"

    category_pk_id = create_Unique_ID()
    category_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Language_form(Base, Base_form):
    __tablename__ = "language"

    language_pk_id = create_Unique_ID()
    language_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Course_Type_form(Base, Base_form):
    __tablename__ = "course_type"

    course_type_pk_id = create_Unique_ID()
    course_type_name = Column(String, index=True, nullable=False, unique=True)
    created_fk_by = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Status_form(Base, Base_form):  # NC: 002
    __tablename__ = "status"
    __table_args__ = (UniqueConstraint('status_name', 'status_cluster'),)

    status_pk_id = create_Unique_ID()

    status_name = Column(String, index=True, nullable=False)
    status_cluster = Column(String, index=True, nullable=False)

    created_fk_by = create_foreignKey("User_form", nullable=True)
    created = relationship("User_form", foreign_keys=[created_fk_by])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teacher_Tardy_report_form(Base, Base_form):
    __tablename__ = "teacher_tardy_report"
    __table_args__ = (UniqueConstraint('teacher_fk_id', 'session_fk_id', 'delay'),)

    teacher_tardy_report_pk_id = create_Unique_ID()
    created_fk_by = create_foreignKey("User_form")

    teacher_fk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    delay = Column(Integer, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    teacher = relationship("User_form", foreign_keys=[teacher_fk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    session = relationship("Session_form", foreign_keys=[session_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Sub_Request_form(Base, Base_form):
    __tablename__ = "sub_request"

    sub_request_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")

    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    main_teacher_fk_id = create_foreignKey("User_form")
    sub_teacher_fk_id = create_foreignKey("User_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    sessions = relationship("Session_form", foreign_keys=[session_fk_id])
    main_teacher = relationship("User_form", foreign_keys=[main_teacher_fk_id])
    sub_teacher = relationship("User_form", foreign_keys=[sub_teacher_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Session_Cancellation_form(Base, Base_form):
    __tablename__ = "session_cancellation"

    session_cancellation_pk_id = create_Unique_ID()

    created_fk_by = create_foreignKey("User_form")

    course_fk_id = create_foreignKey("Course_form")
    sub_course_fk_id = create_foreignKey("Sub_Course_form")
    session_fk_id = create_foreignKey("Session_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    course = relationship("Course_form", foreign_keys=[course_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[sub_course_fk_id])
    session = relationship("Session_form", foreign_keys=[session_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


#class Reassign_Instructor_form(Base, Base_form):
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

class Class_Room:  # NC: 008
    pass


class Branch:  # NC: 008
    pass


class Template_form(Base, Base_form):
    __tablename__ = "templates"
    template_pk_id = create_Unique_ID()
    template_table = Column(String, index=True, nullable=False)
    template_name = Column(String, index=True, nullable=False)
    data = Column(JSON, nullable=False)


class Employee_Salary_form(Base, Base_form):
    __tablename__ = "employee_salary"
    __table_args__ = (UniqueConstraint('user_fk_id', 'year', 'month'),)

    employee_salary_pk_id = create_Unique_ID()
    fingerprint_scanner_user_id = Column(Integer, nullable=True)

    user_fk_id = create_foreignKey("User_form")

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    payment = create_foreignKey("Payment_Method_form", nullable=True)
    payment_date = Column(Date, nullable=True)
    rewards_earning = Column(Float, nullable=False, default=0)
    punishment_deductions = Column(Float, nullable=False, default=0)
    loan_installment = Column(Float, nullable=False, default=0)

    present_time = Column(Integer, nullable=False)
    Regular_hours = Column(Integer, nullable=False)
    Overtime = Column(Integer, nullable=False)
    Undertime = Column(Integer, nullable=False)
    Off_Day = Column(Integer, nullable=False)

    delay = Column(Integer, nullable=False)
    haste = Column(Integer, nullable=False)

    attendance_points = Column(Integer, nullable=False, default=0)
    Fix_pay = Column(Float, nullable=False, default=0)

    Regular_earning = Column(Float, nullable=False)
    Overtime_earning = Column(Float, nullable=False)
    Off_Day_earning = Column(Float, nullable=False)

    Undertime_deductions = Column(Float, nullable=False)
    insurance_deductions = Column(Float, nullable=False)
    tax_deductions = Column(Float, nullable=False)

    remote = Column(Integer, nullable=False)
    vacation_leave = Column(Integer, nullable=False)
    medical_leave = Column(Integer, nullable=False)
    business_trip = Column(Integer, nullable=False)

    remote_earning = Column(Float, nullable=False)
    vacation_leave_earning = Column(Integer, nullable=False)
    medical_leave_earning = Column(Float, nullable=False)
    business_trip_earning = Column(Float, nullable=False)

    total_earning = Column(Float, nullable=False)
    total_deduction = Column(Float, nullable=False)
    total_income = Column(Float, nullable=False)

    Salary_Policy = Column(JSON, nullable=False)
    Days = Column(JSON, nullable=False)

    employee = relationship("User_form", foreign_keys=[user_fk_id])
    card = relationship("Payment_Method_form", foreign_keys=[payment])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Teacher_salary_form(Base, Base_form):
    __tablename__ = "teacher_salary"
    # __table_args__ = (UniqueConstraint('user_fk_id', 'subcourse_fk_id'),)
    teacher_salary_pk_id = create_Unique_ID()

    user_fk_id = create_foreignKey("User_form")
    subcourse_fk_id = create_foreignKey("Sub_Course_form")

    course_data = Column(JSON, nullable=False)
    total_sessions = Column(Integer, nullable=False)

    payment = create_foreignKey("Payment_Method_form", nullable=True)
    payment_date = Column(Date, nullable=True)
    rewards_earning = Column(Float, nullable=False, default=0)
    punishment_deductions = Column(Float, nullable=False, default=0)
    loan_installment = Column(Float, nullable=False, default=0)

    roles_score = Column(Float, nullable=False)
    survey_score = Column(Float, nullable=False)
    course_level_score = Column(Float, nullable=False)
    tardy_score = Column(Float, nullable=False)
    content_creation = Column(Float, nullable=False)
    event_participate = Column(Float, nullable=False)
    CPD = Column(Float, nullable=False)
    Odd_hours = Column(Float, nullable=False)
    report_to_student = Column(Float, nullable=False)
    LP_submission = Column(Float, nullable=False)
    student_assign_feedback = Column(Float, nullable=False)
    result_submission_to_FD = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    SUB = Column(Boolean, nullable=False)
    sub_point = Column(Float, nullable=False)
    ID_Experience = Column(Integer, nullable=False)
    experience_gain = Column(Integer, nullable=False)
    attended_session = Column(Integer, nullable=False)
    roles = Column(JSON, nullable=False)
    score = Column(Float, nullable=False)
    earning = Column(Float, nullable=False)

    BaseSalary = Column(Float, nullable=False)
    session_cancellation_deduction = Column(Float, nullable=False)

    card = relationship("Payment_Method_form", foreign_keys=[payment])
    teacher = relationship("User_form", foreign_keys=[user_fk_id])
    sub_course = relationship("Sub_Course_form", foreign_keys=[subcourse_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)


class Reward_card_form(Base, Base_form):
    __tablename__ = "reward_card"

    reward_card_pk_id = create_Unique_ID()
    user_fk_id = create_foreignKey("User_form")
    created_fk_by = create_foreignKey("User_form")
    reward_amount = Column(Float, nullable=False)
    reward_type = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    created = relationship("User_form", foreign_keys=[created_fk_by])
    employee = relationship("User_form", foreign_keys=[user_fk_id])


class Deleted_Records(Base):
    __tablename__ = "deleted_records"
    deleted_records_pk_id = create_Unique_ID()
    deleted_fk_by = create_foreignKey("User_form", nullable=True)
    table = Column(String, nullable=False)
    rows_data = Column(JSON, nullable=False)


class TEMP_form(Base, Base_form):
    __tablename__ = "temp"
    temp_pk_id = create_Unique_ID()
    key = Column(Integer, default=0)
    value = Column(Integer, default=0)


class Discount_code_form(Base, Base_form):
    __tablename__ = "discount_code"
    discount_code_pk_id = create_Unique_ID()
    discount_code = Column(String, nullable=False, index=True)
    discount_type = Column(String, nullable=False, index=True)  # Fix / Percentage
    discount_amount = Column(Float, nullable=False)

class SignUp_queue(Base):
    __tablename__ = "signup_queue"
    __table_args__ = (UniqueConstraint('student_pk_id', 'subcourse_fk_id'),)
    signup_queue_pk_id = create_Unique_ID()
    student_pk_id = Column(GUID, nullable=False, index=True)
    course_fk_id = Column(GUID, nullable=False, index=True)
    subcourse_fk_id = Column(GUID, nullable=False, index=True)


class SignUp_payment_queue_form(Base, Base_form):
    __tablename__ = "signup_payment_queue"
    __table_args__ = (UniqueConstraint('student_pk_id', 'course_fk_id'),)
    signup_queue_pk_id = create_Unique_ID()

    student_pk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    discount_code = create_foreignKey("Discount_code_form", nullable=True)

    subcourse_fk_ids = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=False)
    package_discount = Column(Float, nullable=False)

    code = relationship("Discount_code_form", foreign_keys=[discount_code])
    student = relationship("User_form", foreign_keys=[student_pk_id])
    course = relationship("Course_form", foreign_keys=[course_fk_id])

class SignUp_form(Base):
    __tablename__ = "signup"
    __table_args__ = (UniqueConstraint('student_pk_id', 'subcourse_fk_id'),)
    signup_pk_id = create_Unique_ID()

    student_pk_id = create_foreignKey("User_form")
    course_fk_id = create_foreignKey("Course_form")
    subcourse_fk_id = create_foreignKey("Sub_Course_form")

    course = relationship("Course_form", foreign_keys=[course_fk_id])
    student = relationship("User_form", foreign_keys=[student_pk_id])
    subcourse = relationship("Sub_Course_form", foreign_keys=[subcourse_fk_id])

    def __repr__(self):
        return Remove_Base_Data(self.__dict__)
