from schemas.Base import *


# Post_Views
class PostViewsBase(BaseModel):
    post_fk_id: int
    ip: str | None = None
    country: str | None = None
    user_creator_fk_id: int = None


class PostViwesCreate(PostViwesBase):
    class Config:
        extra = 'ignore'
        orm_mode = True


class PostViwes(PostViwesBase):
    post_viwe_pk_id: int

    class Config:
        extra = 'ignore'
        orm_mode = True


class UserInPost(BaseModel):
    user_pk_id: int
    fname: str
    lname: str
    image: str
    # gender: str
    deleted: bool

    class Config:
        extra = 'ignore'
        orm_mode = True


# POST

class Post(BaseModel):
    post_summary: str = ""
    post_description: Optional[str] = ""
    post_content: Optional[str] = ""
    post_image: Optional[str] = "defult_post_image.jpg"
    post_direction: Optional[str] = "RTL"

    post_audio_file_link: Optional[str] = None
    post_audio_file_path: Optional[str] = None
    post_aparat_video_id: Optional[str] = None
    post_aparat_video_code: Optional[str] = None
    post_video_file_link: Optional[str] = None
    post_video_file_path: Optional[str] = None
    post_data_file_link: Optional[str] = None
    post_data_file_path: Optional[str] = None
    # users_post_speaker: List[UserInPost] = None
    # users_post_writer: List[UserInPost] = None
    # users_post_actor: List[UserInPost] = None
    # likes: List[LikesInPost] = None
    # comments: List[CommentsInPost] = None
    # views: List[ViwesInPost] = None

    category: Optional[List[UUID]] = []
    tag: Optional[List[UUID]] = []

    users_post_speaker: Optional[List[UUID]] = []
    users_post_writer: Optional[List[UUID]] = []
    users_post_actor: Optional[List[UUID]] = []


class create_post(Post):
    post_old_pk_id: Optional[int]

    post_title: str
    post_type: str

    class Config:
        extra = 'ignore'
        orm_mode = True


class update_post_schema(Post):
    class Config:
        extra = 'ignore'



class post_response_schema(Post):
    category: Optional[Any] = []
    tag: Optional[Any] = []

    users_post_speaker: Optional[Any] = []
    users_post_writer: Optional[Any] = []
    users_post_actor: Optional[Any] = []

    class Config:
        extra = 'ignore'
        orm_mode = True
