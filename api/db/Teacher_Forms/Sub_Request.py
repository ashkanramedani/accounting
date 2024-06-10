from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from lib import logger
from ..Extra import *


# Sub Request
def get_sub_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Sub_Request_form).filter_by(sub_request_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_sub_request(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Sub_Request_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


@not_implemented
def report_sub_request(db: Session, Form: sch.teacher_report):
    try:
        result = (
            db.query(dbm.Sub_Request_form)
            .join(dbm.Course_form, dbm.Course_form.course_pk_id == dbm.Sub_Request_form.course_fk_id)
            .filter_by(deleted=False, teacher_fk_id=Form.teacher_fk_id)
            .filter(dbm.Course_form.course_time.between(Form.start_date, Form.end_date))
            .options(joinedload(dbm.Sub_Request_form.course))
            .all()
        )

        return 200, sum(row.delay for row in result)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_sub_request(db: Session, Form: sch.post_Sub_request_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.sub_teacher_fk_id]):
            return 400, "Bad Request: Employee Not Found"
        logger.warning(db.query(dbm.Session_form.session_pk_id, dbm.Session_form.session_teacher_fk_id).all())
        logger.warning((Form.main_teacher_fk_id, Form.session_fk_id))
        if not db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_fk_id, session_teacher_fk_id=Form.main_teacher_fk_id, deleted=False).first():
            return 400, "Bad Request: session with given teacher not found"

        OBJ = dbm.Sub_Request_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_sub_request(db: Session, form_id):
    try:
        record = db.query(dbm.Sub_Request_form).filter_by(sub_request_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_sub_request(db: Session, Form: sch.update_Sub_request_schema):
    try:
        record = db.query(dbm.Sub_Request_form).filter_by(sub_request_pk_id=Form.sub_request_pk_id, deleted=False)

        if not employee_exist(db, [Form.created_fk_by, Form.main_teacher_fk_id, Form.sub_teacher_fk_id]):
            return 400, "Bad Request"
        if not db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_fk_id, session_teacher_fk_id=Form.main_teacher_fk_id, deleted=False).first():
            return 400, "Bad Request: session with given teacher not found"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def Verify_sub_request(db: Session, Form: sch.Verify_Sub_request_schema):
    try:
        Warn = []
        new_Record = []
        verified = 0
        records = (db.query(dbm.Sub_Request_form)
                   .filter_by(deleted=False)
                   .filter(dbm.Sub_Request_form.sub_request_pk_id.in_(Form.sub_request_pk_id)).all())

        for record in records:
            old_session = db.query(dbm.Session_form).filter_by(session_pk_id=record.session_fk_id, session_teacher_fk_id=record.main_teacher_fk_id, deleted=False)
            if not old_session.first():
                Warn.append(f'{record.session_fk_id}: Session Not Found.')
                continue
            old_session_data = {k: v for k, v in old_session.first().__dict__.items() if k not in ["_sa_instance_state", "is_sub", "session_teacher_fk_id", "session_pk_id", "sub_Request"]}
            new_Record.append(dbm.Session_form(**old_session_data, sub_Request=record.sub_request_pk_id, is_sub=True, session_teacher_fk_id=record.sub_teacher_fk_id))  # type: ignore[call-arg]
            old_session.update({"deleted": True, "sub_Request": record.sub_request_pk_id})
            record.status = 1
            verified += 1

        db.add_all(new_Record)
        db.commit()
        if Warn:
            return 200, f"{verified} Form Verified. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Verified."
    except Exception as e:
        return Return_Exception(db, e)
