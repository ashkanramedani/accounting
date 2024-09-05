from datetime import datetime

import sqlalchemy.sql.expression as sse
from sqlalchemy.orm import Session

from lib import logger



import schemas as sch
import db.models as dbm


# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

# read
def read_all_posts_for_admin_panel(db: Session, topic: str, start_id: int, page_number: int, limit: int):
    try:
        data = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.post_type == topic, dbm.Posts.deleted == False, dbm.Posts.post_pk_id >= start_id)).order_by(dbm.Posts.post_pk_id.desc()).limit(limit).all()
        if data is None:
            return False
        return data
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


def get_post_with_pid(db: Session, pid: str):
    try:
        data = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.post_pk_id == pid, dbm.Posts.deleted == False)).first()
        if data is None:
            return False
        return data
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


# delete
def delete_posts(db: Session, topic: str, pid: int):
    try:
        record = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.deleted == False, dbm.Posts.post_pk_id == pid, dbm.Posts.can_deleted == True)).first()
        if record is not None:
            record.deleted = True
            record.delete_date = datetime.utcnow()
            db.commit()
            return 1
        else:
            return 0
    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


# update
def update_posts(db: Session, topic: str, pid: int, update: dbm.Posts):
    try:
        record = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.deleted == False, dbm.Posts.post_pk_id == pid, dbm.Posts.can_update == True)).first()
        if record is not None:
            record.post_status = update.post_status
            db.commit()
            return 1
        else:
            return 0

    except Exception as e:
        logger.error(e)
        db.rollback()
        return -1


# insert
def create_post(db: Session, new: sch.PostCreate):
    try:
        # category: Optional[List[str]]=[]
        # tag: Optional[List[str]]=[]
        # users_post_speaker: Optional[List[str]]=[]
        # users_post_writer: Optional[List[str]]=[]
        # users_post_actor: Optional[List[str]]=[]
        # validation post_type

        data = dbm.Posts(
                post_title=new.post_title,
                visible=new.visible,
                post_summary=new.post_summary,
                post_type=new.post_type,
                expire_date=new.expire_date,
                post_direction=new.post_direction,
                priority=new.priority,
                post_content=new.post_content,
                post_image=new.post_image,
                user_creator_fk_id=new.user_creator_fk_id,
                post_data_file_path=new.post_data_file_path,
                post_data_file_link=new.post_data_file_link,
                post_video_file_path=new.post_video_file_path,
                post_video_file_link=new.post_video_file_link,
                post_aparat_video_code=new.post_aparat_video_code,
                post_aparat_video_id=new.post_aparat_video_id,
                post_audio_file_path=new.post_audio_file_path,
                post_audio_file_link=new.post_audio_file_link
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        logger.error(e)
        db.rollback()
        return False

# select
# def get_all_posts_with_limit(db:Session, topic:str, limit:int):   
#     data = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.post_type == topic, dbm.Posts.deleted == False)).order_by(dbm.Posts.post_pk_id.desc()).limit(limit).all()
#     if data is None:
#         return False
#     return data

# def get_all_posts_with_page_and_limit(db:Session, topic:str, limit:int, page:int):   
#     ids = db.query(dbm.Posts.post_pk_id).filter(sse.and_(dbm.Posts.post_type == topic, dbm.Posts.deleted == False, dbm.Posts.post_status == 1)).order_by(dbm.Posts.post_pk_id.desc()).all()
#     if page * limit > len(ids):
#         return []
#     data = db.query(dbm.Posts).filter(sse.and_(dbm.Posts.post_pk_id <= ids[page*limit].post_pk_id, dbm.Posts.post_pk_id >= ids[min(page*limit+limit, len(ids)-1)].post_pk_id, dbm.Posts.post_type == topic, dbm.Posts.deleted == False, dbm.Posts.post_status == 1)).order_by(dbm.Posts.post_pk_id.desc()).limit(limit).all()
#     if data is None:
#         return False
#     return data

# def get_post_with_topic_and_user_id(db:Session, uid:int, topic:str, limit:int):
#     sql = text(f' SELECT * FROM tbl_posts WHERE tbl_posts.post_pk_id in ( SELECT rel_users_posts.post_id FROM rel_users_posts WHERE rel_users_posts.user_id = {uid} ) and tbl_posts."type" = \'{topic}\' ORDER BY tbl_posts.post_pk_id DESC limit {limit}')
#     data = db.execute(sql)
#     datas = [row for row in data]
#     if datas is None:
#         return False
#     return datas

# def get_viwe(db:Session, id:int):
#     data = db.query(dbm.PostViwes).filter(sse.and_(dbm.PostViwes.post_fk_id == id)).limit(501).all()
#     if data is None:
#         return False
#     return data

# def put_viwe(db:Session, d:sch.PostViwesCreate):
#     try:
#         data = dbm.PostViwes(
#            post_fk_id = d.post_fk_id,
#            ip = d.ip,
#            country = d.country,
#            meta_data = {},
#            user_creator_fk_id = d.user_creator_fk_id
#         )
#         db.add(data)
#         db.commit()
#         db.refresh(data)
#         return  data
#     except Exception as e:
#         logger.error(e)
#         db.rollback()
#         return False
