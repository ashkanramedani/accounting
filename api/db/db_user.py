import sqlalchemy.sql.expression as sse
from sqlalchemy.orm import Session

from lib import log

logger = log()
import db.models as dbm


# expier_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

def get_users_withfilter_employes(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(dbm.Users).filter(sse.and_(dbm.Users.deleted == False, dbm.Users.visible == True, dbm.Users.employed == True)).offset(skip).limit(limit).all()

# def get_users_withfilter_not_employes(db: Session, skip: int = 0, limit: int = 100):
#     data = db.query(dbm.Users).filter(sse.and_(dbm.Users.deleted == False, dbm.Users.visible == True, dbm.Users.employed==False)).offset(skip).limit(limit).all()
#     if data is None:
#         return False
#     return data

# def get_user_with_auth_id(db: Session, auth_id: int):
#     data = db.query(dbm.Users).filter(sse.and_(dbm.Users.authentication_fk_id == auth_id, dbm.Users.deleted == False)).first()
#     if data is None:
#         return False
#     return data

# def get_user_by_email(db: Session, email: str):
#     data = db.query(dbm.Users).filter(sse.and_(dbm.Users.email == email, dbm.Users.deleted == False)).first()
#     if data is None:
#         return False
#     return data

# def get_user_by_id(db: Session, id: int):
#     data = db.query(dbm.Users).filter(sse.and_(dbm.Users.user_pk_id == id, dbm.Users.deleted == False)).first()
#     if data is None:
#         return False
#     return data

# def get_user_by_mobile_number(db: Session, mobile_number: str):
#     data = db.query(dbm.Users).filter(sse.and_(dbm.Users.mobile_number == mobile_number, dbm.Users.deleted == False)).first()
#     logger.error(data)
#     if data is None:
#         return False
#     return data

# def put_role_for_user(db: Session, user=sch.User, role=sch.RoleForUser, educational_institution=sch.EducationalInstitution):
#     if user is not None and role is not None:
#         assoc = dbm.UserRole(user=user, role=role, educational_institution=educational_institution)
#         # user_created.roles_user = [role]
#         db.add_all([user, assoc])
#         db.commit()
#         db.refresh(user)
#         db.refresh(assoc)

#     return user

# def put_user(db: Session, new: sch.UserCreate, branch_fk_id:int, gender_fk_id:int, role:sch.RoleForUser, educational_institution:sch.EducationalInstitution):  
#     try:
#         user_created = dbm.Users(
#             fname=new.fname, 
#             lname=new.lname, 
#             mobile_number=new.mobile_number, 
#             email=new.email, 
#             image=new.image, 
#             panel_image=new.image, 
#             branch_fk_id=branch_fk_id,
#             gender_fk_id=gender_fk_id,
#             employed=True,
#             authentication_fk_id=new.authentication_fk_id
#         )
#         assoc = dbm.UserRole(user=user_created, role=role, educational_institution=educational_institution)
#         user_created.roles_user = [role]
#         db.add_all([user_created, assoc])
#         db.commit()
#         db.refresh(user_created)
#         db.refresh(assoc)
#         return user_created
#     except ValueError as e:
#         logger.error(e)
#         db.rollback()
#         return -1 

# def put_user_with_auth_student(db: Session, new: sch.UserCreateAuth, branch_fk_id:int, gender_fk_id:int, role:sch.RoleForUser, educational_institution:sch.EducationalInstitution, auth_fk_id: int):  
#     try:
#         user_created = dbm.Users(
#             fname=new.fname, 
#             lname=new.lname, 
#             mobile_number=new.mobile_number, 
#             email=new.email, 
#             image='male.webp', 
#             panel_image='male.webp', 
#             branch_fk_id=branch_fk_id,
#             gender_fk_id=gender_fk_id,
#             employed=True,
#             authentication_fk_id=auth_fk_id
#         )

#         assoc = dbm.UserRole(user=user_created, role=role, educational_institution=educational_institution)
#         user_created.roles_user = [role]
#         db.add_all([user_created, assoc])
#         db.commit()
#         db.refresh(user_created)
#         db.refresh(assoc)
#         return user_created
#     except ValueError as e:
#         logger.error(e)
#         db.rollback()
#         return -1 

# def delete_user(db: Session, _id: int):
#     try:
#         record = db.query(dbm.Users).filter(sse.and_(dbm.Users.deleted == False, dbm.Users.user_pk_id == _id)).first()
#         if record is not None:

#             record_rel = db.query(dbm.UserRole).filter(sse.and_(dbm.UserRole.user_fk_id == record.user_pk_id)).first()
#             db.delete(record_rel)
#             db.commit()

#             record_auth = db.query(dbm.Authentications).filter(sse.and_(dbm.Authentications.authentication_pk_id == record.authentication_fk_id)).first()
#             db.delete(record_auth)
#             db.commit()

#             record.deleted = True
#             record.visible = False
#             record.employed = False
#             record.delete_date = datetime.utcnow()            
#             db.commit()

#             return 1   
#         else:
#             return 0
#     except Exception as e:
#         logger.error(e)
#         db.rollback()
#         return -1 


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     data = db.query(dbm.User).offset(skip).limit(limit).all()
#     if data is None:
#         return False
#     return data


# # def update_users(db: Session, _id: int, update_obj: Users):
# #     return 


# # # insert
# # def put_user(db: Session, new_obj: UserBase, roles: List[int]=[]):
# #     try:
# #         user = Users(        
# #             fname = new_obj.fname,
# #             lname = new_obj.lname,    
# #             email = new_obj.email,
# #             mobile_number = new_obj.mobile_number,
# #             image = new_obj.image,
# #             gender = new_obj.gender
# #         )
# #         db.add(user)
# #         db.commit()
# #         db.refresh(user)

# #         if user.id and user.id > 0:
# #             for i in range(len(roles)):
# #                 try:
# #                     _role = db.query(Roles.id).filter(Roles.id == roles[i]).first()
# #                     user.roles = [_role]
# #                     role_rel_user = users_roles_association(
# #                         user_id = user.id,
# #                         role_id = roles[i]
# #                     )
# #                     db.add(role_rel_user)
# #                     db.commit()
# #                     db.refresh(role_rel_user)
# #                 except Exception as e:
# #                     logger.error(e)

# #             au = Authentications(
# #                 password=Hash._bcrypt(new_obj.password),
# #                 username=new_obj.username,
# #                 user_id=user.id
# #             )
# #             db.add(au)
# #             db.commit()
# #             db.refresh(au)
# #         return user.id

# #     except Exception as e:
# #         logger.error(e)
# #         db.rollback()
# #         return -1 


# # # select

# # def get_all_without_employees(db:Session):
# #     return db.query(Users).filter(sse.and_(Users.deleted==False, Users.employed==False)).order_by(Users.id.desc()).all()

# # def get_all_just_employees(db:Session):
# #     return db.query(Users).filter(sse.and_(Users.deleted==False, Users.employed==True)).order_by(Users.id.desc()).all()

# # def get_user_by_username(username, db:Session):
# #     au = db.query(Authentications).filter(Authentications.username == username).first()
# #     user = db.query(Users).filter(sse.and_(Users.id == au.user_id, Users.deleted == False)).first()
# #     return user

# # def me(db: Session, user_id):
# #     return db.query(Users).filter(Users.id == user_id).first()
