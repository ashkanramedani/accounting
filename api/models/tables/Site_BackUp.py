from sqlalchemy import func, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import expression

from .Base_form import *

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


# class Authentications(Base, Base_form):
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
