from lib import logger



from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from .Extra import *


# Tardy Form - get_tardy_request

# Teacher Replacement
def get_teacher_replacement(db: Session, form_id):
    try:
        return 200, db.query(dbm.Teacher_Replacement_form).filter_by(teacher_replacement_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_teacher_replacement(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Teacher_Replacement_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def report_teacher_replacement(db: Session, Form: sch.teacher_report):
    try:
        result = (
            db.query(dbm.Teacher_Replacement_form)
            .join(dbm.Class_form, dbm.Class_form.class_pk_id == dbm.Teacher_Replacement_form.class_fk_id)
            .filter_by(deleted=False, teacher_fk_id=Form.teacher_fk_id)
            .filter(dbm.Class_form.class_time.between(Form.start_date, Form.end_date))
            .options(joinedload(dbm.Teacher_Replacement_form.course))
            .count()
        )

        return 200, result
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_teacher_replacement(db: Session, Form: sch.post_teacher_replacement_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id, Form.replacement_teacher_fk_id]):
            return 400, "Bad Request"
        if not class_exist(db, Form.class_fk_id):
            return 400, "Bad Request"

        OBJ = dbm.Teacher_Replacement_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_teacher_replacement(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Replacement_form).filter_by(teacher_replacement_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_teacher_replacement(db: Session, Form: sch.update_teacher_replacement_schema):
    try:
        record = db.query(dbm.Teacher_Replacement_form).filter_by(teacher_replacement_pk_id=Form.teacher_replacement_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id, Form.replacement_teacher_fk_id]):
            return 400, "Bad Request"
        if not class_exist(db, Form.class_fk_id):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
