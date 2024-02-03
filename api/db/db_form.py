import logging
from uuid import UUID

from sqlalchemy.orm import Session

import schemas as sch
import db.models as dbm

# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

__all__ = [
    "get_leave_request",
    "post_leave_request",
    "delete_leave_request",
    "update_leave_request",
    "get_tardy_request",
    "post_tardy_request",
    "delete_tardy_request",
    "update_tardy_request",
    "get_all_leave_request"
]


# Leave Request
def get_leave_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_leave_request(db: Session):
    try:
        data = db.query(dbm.Leave_request_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_leave_request(db: Session, Form: sch.post_leave_request_schema):
    try:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=Form.created_by, deleted=False).first() or not db.query(dbm.Employees_form).filter_by(employees_pk_id=Form.created_for, deleted=False).first():
            return 404, "Target Employee Not Found"
        OBJ = dbm.Leave_request_form(
                created_by_fk_id=Form.created_by,
                created_for_fk_id=Form.created_for,
                start_date=Form.start_date,
                end_date=Form.end_date,
                Description=Form.Description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_leave_request(db: Session, Form: sch.delete_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=Form.form_id,
                deleted=False
        ).delete()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_leave_request(db: Session, Form: sch.update_leave_request_schema):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=Form.leave_request_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.created_by_fk_id = Form.created_by
        record.created_for_fk_id = Form.created_for
        record.Start_Date = Form.start_date,
        record.End_Date = Form.end_date,
        record.Description = Form.Description
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# Tardy Form


def get_tardy_request(db: Session, Form: sch.get_teacher_tardy_reports_schema):
    try:
        if isinstance(Form.teacher_tardy_reports_pk_id, UUID):
            data = (db
                    .query(dbm.Teacher_tardy_reports_form)
                    .filter(dbm.Teacher_tardy_reports_form.teacher_tardy_reports_pk_id == Form.teacher_tardy_reports_pk_id)
                    .first())
        else:
            data = db.query(dbm.Teacher_tardy_reports_form).all()
        if data:
            return 200, data
        return 404, f"Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        OBJ = dbm.Teacher_tardy_reports_form(
                created_fk_by=Form.created_fk_by,
                teacher_fk_id=Form.teacher_fk_id,
                class_fk_id=Form.class_fk_id,
                delay=Form.delay
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_tardy_request(db: Session, Form: sch.delete_teacher_tardy_reports_schema):
    try:
        record = (db
                  .query(dbm.Teacher_tardy_reports_form)
                  .filter(dbm.Teacher_tardy_reports_form.teacher_tardy_reports_pk_id == Form.teacher_tardy_reports_pk_id)
                  .first())
        if not record or record.deleted:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "employee Deleted"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = (((db
                    .query(dbm.Teacher_tardy_reports_form))
                   .filter(dbm.Teacher_tardy_reports_form.teacher_tardy_reports_pk_id == Form.teacher_tardy_reports_pk_id))
                  .first())
        if not record:
            return 404, "Not Found"

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
