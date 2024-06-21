from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import logger
from ..Extra import *


# Sub Request
def get_session_cancellation(db: Session, form_id):
    try:
        return 200, db.query(dbm.Session_Cancellation_form).filter_by(session_cancellation_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_session_cancellation(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Session_Cancellation_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


# @not_implemented
# def report_session_cancellation(db: Session, Form: sch.teacher_report):
#     try:
#         result = (
#             db.query(dbm.Session_Cancellation_form)
#             .join(dbm.Course_form, dbm.Course_form.course_pk_id == dbm.Session_Cancellation_form.course_fk_id)
#             .filter_by(deleted=False, teacher_fk_id=Form.teacher_fk_id)
#             .filter(dbm.Course_form.course_time.between(Form.start_date, Form.end_date))
#             .options(joinedload(dbm.Session_Cancellation_form.course))
#             .all()
#         )
#
#         return 200, sum(row.delay for row in result)
#     except Exception as e:
#         logger.error(e)
#         db.rollback()
#         return 500, f'{e.__class__.__name__}: {e.args}'


def post_session_cancellation(db: Session, Form: sch.post_Session_Cancellation_schema):
    try:
        session = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_fk_id, deleted=False)
        if not session:
            return 400, "Session not found"
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: Employee Not Found"

        OBJ = dbm.Session_Cancellation_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_session_cancellation(db: Session, form_id):
    try:
        record = db.query(dbm.Session_Cancellation_form).filter_by(session_cancellation_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_session_cancellation(db: Session, Form: sch.update_Session_Cancellation_schema):
    try:
        record = db.query(dbm.Session_Cancellation_form).filter_by(session_cancellation_pk_id=Form.session_cancellation_pk_id, deleted=False)

        if not record:
            return 400, "Record Not Found"
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: Employee Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def Verify_session_cancellation(db: Session, Form: sch.Verify_Session_Cancellation_schema):
    try:
        Warn = []
        new_Record = []
        verified = 0
        records = db \
            .query(dbm.Session_Cancellation_form) \
            .filter_by(deleted=False) \
            .filter(dbm.Session_Cancellation_form.session_cancellation_pk_id.in_(Form.session_cancellation_pk_id)) \
            .all()

        for record in records:
            old_session = db.query(dbm.Session_form).filter_by(session_pk_id=record.session_fk_id, deleted=False)
            if not old_session.first():
                Warn.append(f'{record.session_fk_id}: Session Not Found.')
                continue

            old_session.canceled = True
            record.status = 1   # NC: 004
            verified += 1

        db.add_all(new_Record)
        db.commit()
        if Warn:
            return 200, f"{verified} Form Verified. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Verified."
    except Exception as e:
        return Return_Exception(db, e)
