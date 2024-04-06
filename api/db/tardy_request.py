from lib import logger



from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from .Extra import *


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_tardy_request(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Teacher_tardy_reports_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def report_tardy_request(db: Session, Form: sch.teacher_report):
    try:
        result = (
            db.query(dbm.Teacher_tardy_reports_form)
            .join(dbm.course_form, dbm.course_form.course_pk_id == dbm.Teacher_tardy_reports_form.course_fk_id)
            .filter_by(deleted=False, teacher_fk_id=Form.teacher_fk_id)
            .filter(dbm.course_form.course_time.between(Form.start_date, Form.end_date))
            .options(joinedload(dbm.Teacher_tardy_reports_form.course))
            .all()
        )

        return 200, sum(row.delay for row in result)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request"
        if not course_exist(db, Form.course_fk_id):
            return 400, "Bad Request"

        OBJ = dbm.Teacher_tardy_reports_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(teacher_tardy_reports_pk_id=Form.teacher_tardy_reports_pk_id, deleted=False)

        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request"
        if not course_exist(db, Form.course_fk_id):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
