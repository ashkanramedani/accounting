from schemas.Base import *


class Library(BaseModel):
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


class post_library(Library):
    pass

    class Config:
        extra = 'ignore'
        orm_mode = True
