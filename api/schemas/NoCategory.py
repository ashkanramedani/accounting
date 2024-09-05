from .Base import *

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int


# -------------------   Authentications   -------------------
# class  AuthenticationBase(BaseModel):
#     username: str
#     password: str
# class  AuthenticationCreate(AuthenticationBase):
#     class  Config:
#         orm_mode = True
# class  Authentication(AuthenticationBase):
#     authentication_pk_id: int
#     class  Config:
#         orm_mode = True
# class  AuthenticationWithoutPassword(BaseModel):
#     username: str
#     authentication_pk_id: int
#     class  Config:
#         orm_mode = True
# class  AuthenticationLogin(BaseModel):
#     user_pk_id: Optional[int]
#     username: Optional[str]
#     mobile_number: Optional[str]
#     has_account: Optional[bool] = False
#     has_password: Optional[bool] = False
#     login_method: Optional[str]
#     otp_send_successful: Optional[bool]
#     email_send_successful: Optional[bool]

#     class  Config:
#         orm_mode = True
# class  Token(BaseModel):
#     user_pk_id: Optional[int]
#     refresh_token: Optional[str]
#     access_token: Optional[str]
#     type_token: Optional[str]
#     login_method: Optional[str]

#     class  Config:
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


# class  UserCreateAuth(BaseModel):
#     # password: str
#     fname: str
#     lname: str
#     mobile_number: str
#     email: str
#     class  Config:
#         orm_mode = True
# class  CandidateInfoForReport(BaseModel):
#     user_pk_id: int
#     mobile_number: str
#     email: str
#     image: str
#     fname: str
#     national_id: Optional[str] = ""
#     lname: str
#     class  Config:
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
    create_date: datetime | str
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
    create_date: datetime | str


class LibraryCreate(LibraryBase):
    pass
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

