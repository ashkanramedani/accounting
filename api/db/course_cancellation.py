from lib import logger
from sqlalchemy.orm import Session
import db.models as dbm
import schemas as sch
from .Extra import *





# course_cancellation
def get_course_cancellation_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.course_Cancellation_form).filter_by(course_cancellation_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_course_cancellation_form(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.course_Cancellation_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'



def report_course_cancellation(db: Session, Form: sch.teacher_report):
    try:
        result = (
            db.query(dbm.course_Cancellation_form)
            .filter_by(deleted=False, employee_fk_id= Form.teacher_fk_id)
            .filter(dbm.course_Cancellation_form.end_date.between(Form.start_date, Form.end_date))
            .count()
        )

        return 200, result
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'

def post_course_cancellation_form(db: Session, Form: sch.post_course_cancellation_schema):
    try:
        if not employee_exist(db, [Form.teacher_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        if not course_exist(db, Form.course_fk_id):
            return 400, "Bad Request"

        OBJ = dbm.course_Cancellation_form(**Form.dict())  # type: ignore[call-arg]  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"

    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_course_cancellation_form(db: Session, form_id):
    try:
        record = db.query(dbm.course_Cancellation_form).filter_by(course_cancellation_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_course_cancellation_form(db: Session, Form: sch.update_course_cancellation_schema):
    try:
        record = db.query(dbm.course_Cancellation_form).filter_by(course_cancellation_pk_id=Form.course_cancellation_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.teacher_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        if not course_exist(db, Form.course_fk_id):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
