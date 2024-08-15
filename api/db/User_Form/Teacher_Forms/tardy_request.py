from uuid import UUID

from sqlalchemy.orm import Session, joinedload

import schemas as sch
from db import models as dbm
from db.Extra import *
from lib import logger


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:

        return 200, db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_report_pk_id=form_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_tardy_request(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Teacher_Tardy_report_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def report_tardy_request(db: Session, subcourse_id: UUID):
    try:
        return 200, db.query(dbm.Teacher_Tardy_report_form).filter_by(sub_course_fk_id=subcourse_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").all()
    except Exception as e:
        return Return_Exception(db, e)

def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request: Employee Not Found"

        target_session = db.query(dbm.Session_form).filter_by(session_pk_id=Form.session_fk_id).filter(dbm.Session_form.status != "deleted").first()
        if not target_session:
            return 400, "Bad Request: session not found"

        Full_Details = {
            "teacher_fk_id": target_session.session_teacher_fk_id,
            "course_fk_id": target_session.course_fk_id,
            "sub_course_fk_id": target_session.sub_course_fk_id,
            "session_fk_id": target_session.session_pk_id
        }

        OBJ = dbm.Teacher_Tardy_report_form(delay=Form.delay, created_fk_by=Form.created_fk_by, **Full_Details)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_report_pk_id=form_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_report_pk_id=Form.teacher_tardy_report_pk_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted")

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        # record.update(Form.dict(), synchronize_session=False)
        record.first().delay = Form.delay
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)

def verify_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_report_pk_id=form_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.status = Set_Status(db, "form", "verified")
        db.commit()
        return 200, "Verified"
    except Exception as e:
        return Return_Exception(db, e)
