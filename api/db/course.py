from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from .Extra import *


def get_course(db: Session, course_id):
    try:
        return 200, db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_course(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.course_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_course(db: Session, Form: sch.post_course_schema):
    try:
        data = Form.dict()
        teachers = data.pop("teachers")

        if not teachers:
            return 200, "course with no teacher added"

        OBJ = dbm.course_form(**data)  # type: ignore[call-arg]
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        teacher_ID: List[UUID] = [ID.employees_pk_id for ID in db.query(dbm.Employees_form).filter_by(deleted=False).all()]

        for teacher_id in teachers:
            if teacher_id not in teacher_ID:
                return 400, "Bad Request: teacher not found"
            OBJ.teachers.append(db.query(dbm.Employees_form).filter_by(employees_pk_id=teacher_id, deleted=False).first())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "course Added"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_course(db: Session, course_id):
    try:
        record = db.query(dbm.course_form).filter_by(course_pk_id=course_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_course(db: Session, Form: sch.update_course_schema):
    try:
        record = db.query(dbm.course_form).filter_by(course_pk_id=Form.course_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
