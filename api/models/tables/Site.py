from sqlalchemy import Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .Base_form import *

users_departments_association = Table(
        'rel_users_departments',
        Base.metadata,
        create_foreignKey("User_form", name="user_fk_id"),
        create_foreignKey("Departments_form", name="department_fk_id"),
        create_foreignKey("Educational_institutions_form", name="educational_institution_fk_id"))

users_posts_actor_association = Table(
        'rel_users_posts_actor',
        Base.metadata,
        create_foreignKey("User_form", name="user_fk_id"),
        create_foreignKey("Posts_form", name="post_fk_id"))

users_posts_writer_association = Table(
        'rel_users_posts_writer',
        Base.metadata,
        create_foreignKey("User_form", name="user_fk_id"),
        create_foreignKey("Posts_form", name="post_fk_id"))

users_posts_speaker_association = Table(
        'rel_users_posts_speaker',
        Base.metadata,
        create_foreignKey("User_form", name="user_fk_id"),
        create_foreignKey("Posts_form", name="post_fk_id"))

PostTag = Table(
        "post_tag",
        Base.metadata,
        create_foreignKey("Tag_form", name="tag_fk_id"),
        create_foreignKey("Posts_form", name="post_fk_id"),
        UniqueConstraint("tag_fk_id", "post_fk_id"), )

PostCategory = Table(
        "post_category",
        Base.metadata,
        create_foreignKey("Category_form", name="category_fk_id"),
        create_foreignKey("Posts_form", name="post_fk_id"),
        UniqueConstraint("category_fk_id", "course_fk_id"), )


class Departments_form(Base, Base_form):
    __tablename__ = "departments_form"
    departments_form_pk_id = create_Unique_ID()


class Exam_template_form(Base, Base_form):
    __tablename__ = "exam_template"
    exam_template_pk_id = create_Unique_ID()


class Educational_institutions_form(Base, Base_form):
    __tablename__ = "educational_institutions"
    educational_institutions_pk_id = create_Unique_ID()



class PostViews(Base, Base_form):
    __tablename__ = "tbl_post_views"

    post_view_pk_id = create_Unique_ID()
    post_view_old_pk_id = create_OLD_id()

    ip = Column(String(250), default=None)
    country = Column(String(250), default=None)
    meta_data = Column(JSONB, server_default='{}')

    post_fk_id = create_foreignKey("Posts_form")
    created_fk_by = create_foreignKey("User_form")
    educational_institution_fk_id = create_foreignKey("Educational_institutions_form")

    post = relationship("Posts_form", foreign_keys=[post_fk_id])
    created = relationship("User_form", foreign_keys=[created_fk_by])
    educational_institution = relationship("User_form", foreign_keys=[educational_institution_fk_id])


class Posts_form(Base, Base_form):
    __tablename__ = "posts"

    post_pk_id = create_Unique_ID()
    post_old_pk_id = create_OLD_id()

    post_title = Column(String)
    post_summary = Column(String)
    post_description = Column(String)
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

    post_tags = relationship("Tag_form", secondary=PostTag, backref="post_tag")
    post_categories = relationship("Category_form", secondary=PostCategory, backref="post_category")

    created_fk_by = create_foreignKey("User_form")
    educational_institution_fk_id = create_foreignKey("Educational_institutions_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    educational_institution = relationship("Educational_institutions_form", foreign_keys=[educational_institution_fk_id])

    # users_post_speaker = relationship("Users", secondary=users_posts_speaker_association)
    # users_post_writer = relationship("Users", secondary=users_posts_writer_association)
    # users_post_actor = relationship("Users", secondary=users_posts_actor_association)
    # post_view = relationship("Users", secondary=users_posts_writer_association)

    # comments = relationship("PostComments", backref="rel_comments")
    # list_views = relationship("PostViews", backref="rel_views")
    # likes = relationship("PostLikes", backref="rel_likes")


class Library_form(Base, Base_form):
    __tablename__ = "library"

    library_pk_id = create_Unique_ID()
    library_old_pk_id = create_OLD_id()

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

    created_fk_by = create_foreignKey("User_form")
    educational_institution_fk_id = create_foreignKey("Educational_institutions_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    educational_institution = relationship("Educational_institutions_form", foreign_keys=[educational_institution_fk_id])

class Exams_form(Base, Base_form):
    tablename = 'exams'

    exam_pk_id = create_Unique_ID()
    exam_old_pk_id = create_OLD_id()

    exam_name = Column(String, nullable=False, default="")
    exam_type = Column(String, nullable=False, default="", index=True)
    exam_price = Column(Integer, nullable=False, default=0)
    exam_image = Column(String, nullable=False, default="default.webp")
    exam_level = Column(String, nullable=False, default="")
    exam_description = Column(String, nullable=False, default="")
    exam_offer_percent = Column(Integer, default=0)
    exam_offer_price = Column(Integer, default=0)
    exam_tax = Column(Float, default=0.09)
    exam_capacity = Column(Integer, default=0)

    created_fk_by = create_foreignKey("User_form")
    language_fk_id = create_foreignKey("Language_form")
    exam_template_fk_id = create_foreignKey("Exam_template_form")
    educational_institution_fk_id = create_foreignKey("Educational_institutions_form")

    created = relationship("User_form", foreign_keys=[created_fk_by])
    language = relationship("Language_form", foreign_keys=[language_fk_id])
    exam_template = relationship("Exam_template_form", foreign_keys=[exam_template_fk_id])
    educational_institution = relationship("Educational_institutions_form", foreign_keys=[educational_institution_fk_id])
