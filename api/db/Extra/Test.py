from contextlib import contextmanager
from typing import List, Any, Dict
from uuid import UUID
from schemas import course_data_for_report
from fastapi import APIRouter
from fastapi import FastAPI
from starlette.testclient import TestClient

from lib import logger
from schemas import Route_Result
from db import models as dbm
from sqlalchemy import select, join, and_
from sqlalchemy.orm import aliased, joinedload

# Assuming the models are defined as User, Role, and UsersRoles


from sqlalchemy.orm import Session
from sqlalchemy.sql import true


def TestRoute_2(db: Session):



    # Assuming the models are defined as User, Role, and UsersRoles


    stmt = (
        db.query(
                dbm.User_form.name.label("username"),
                dbm.User_form.last_name.label("user_lastname"),
                dbm.Role_form.name.label("role_name"),
                dbm.Role_form.cluster.label("role_Cluster")
        )

        .select_from(dbm.User_form)
        .join(
                dbm.Role_form,
                dbm.UserRole.c.role_fk_id == dbm.Role_form.role_pk_id
        )
        .join(
                dbm.UserRole,
                and_(
                        dbm.UserRole.c.role_fk_id == dbm.Role_form.role_pk_id,
                        dbm.UserRole.c.user_fk_id == dbm.User_form.user_pk_id
                )
        )
    )

    logger.debug(stmt)

    return stmt.all()
    # q = db.query(dbm.Role_form)
    # return q
        # \
        # .filter(User.id == u.id))

    # # teacher_roles_Query: List[dbm.UserRole] = db.query(dbm.UserRole).filter(dbm.UserRole.user_fk_id.in_(Teachers.keys())).all()
    # teacher_roles_Query: List[dbm.UserRole] = db \
    #     .query(dbm.UserRole) \
    #     .join(dbm.Role_form).all()



from pydantic import BaseModel

class USER(BaseModel):
    user_pk_id: UUID
    roles: Any

    class Config:
        orm_mode = True
        extra = "ignore"

class Course(BaseModel):
    type: Any

    class Config:
        orm_mode = True
        extra = "ignore"


def create_Report(data: Dict):
    role_data: List = data.pop("roles", [])
    if role_data:
        data["roles"] = {i.name: i.value for i in role_data}
        data["Role_Score"] = sum(i.value for i in role_data)
    return data


def TestRoute(db: Session):
    course_data = db.query(dbm.Course_form).options(joinedload(dbm.Course_form.type)).first()

    return course_data_for_report(**course_data.__dict__)


"""
SELECT
	course.course_type AS course_course_type,
	course.course_capacity AS course_course_capacity,
	course.course_level AS course_course_level,
	course_type_table.course_type_name AS course_type_table_course_type_name,
FROM
	course
	LEFT OUTER 
	JOIN course_type AS course_type_table 
	ON course_type_table.course_type_pk_id = course.course_type

"""
