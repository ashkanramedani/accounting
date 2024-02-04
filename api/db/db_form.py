import logging
from uuid import UUID

from sqlalchemy.orm import Session
from typing import List
import schemas as sch
import db.models as dbm

__all__ = [
    "get_leave_request",
    "get_all_leave_request",
    "post_leave_request",
    "delete_leave_request",
    "update_leave_request",
    "get_tardy_request",
    "get_all_tardy_request",
    "post_tardy_request",
    "delete_tardy_request",
    "update_tardy_request",
    "get_teacher_replacement",
    "get_all_teacher_replacement",
    "post_teacher_replacement",
    "delete_teacher_replacement",
    "update_teacher_replacement",
    "get_business_trip_form",
    "get_all_business_trip_form",
    "post_business_trip_form",
    "delete_business_trip_form",
    "update_business_trip_form",
    "get_class_cancellation_form",
    "get_all_class_cancellation_form",
    "post_class_cancellation_form",
    "delete_class_cancellation_form",
    "update_class_cancellation_form",
    "get_remote_request_form",
    "get_all_remote_request_form",
    "post_remote_request_form",
    "delete_remote_request_form",
    "update_remote_request_form"
]


def employee_exist(db: Session, FK_fields: List[UUID]):
    for FK_field in FK_fields:
        if not db.query(dbm.Employees_form).filter_by(employees_pk_id=FK_field, deleted=False).first():
            return False
    return True


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
        if not employee_exist(db, [Form.created_by, Form.created_for]):
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
        ).first()
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
            return 404, "Form Not Found"

        if not employee_exist(db, [Form.created_by, Form.created_for]):
            return 404, "Target Employee Not Found"

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


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(
                teacher_tardy_reports_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_tardy_request(db: Session):
    try:
        data = db.query(dbm.Teacher_tardy_reports_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.create_by_fk_id, Form.teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"
        OBJ = dbm.Teacher_tardy_reports_form(
                create_by_fk_id=Form.create_by_fk_id,
                teacher_fk_id=Form.teacher_fk_id,
                class_fk_id=Form.class_fk_id,
                delay=Form.delay
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Leave_request_form).filter_by(
                leave_request_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_tardy_reports_form).filter_by(
                teacher_tardy_reports_pk_id=Form.teacher_tardy_reports_pk_id,
                deleted=False
        ).first()

        if not employee_exist(db, [Form.create_by_fk_id, Form.teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        if not record:
            return 404, "Not Found"
        record.create_by_fk_id = Form.create_by_fk_id,
        record.teacher_fk_id = Form.teacher_fk_id,
        record.class_fk_id = Form.class_fk_id,
        record.delay = Form.delay
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# Teacher Replacement
def get_teacher_replacement(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Replacement_form).filter_by(
                teacher_replacement_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_teacher_replacement(db: Session):
    try:
        data = db.query(dbm.Teacher_Replacement_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_teacher_replacement(db: Session, Form: sch.post_teacher_replacement_schema):
    try:
        if not employee_exist(db, [Form.created_by_fk_id, Form.teacher_fk_id, Form.replacement_teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        OBJ = dbm.Teacher_Replacement_form(
                created_by_fk_id=Form.created_by_fk_id,
                teacher_fk_id=Form.teacher_fk_id,
                replacement_teacher_fk_id=Form.replacement_teacher_fk_id,
                class_fk_id=Form.class_fk_id
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_teacher_replacement(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Replacement_form).filter_by(
                teacher_replacement_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_teacher_replacement(db: Session, Form: sch.update_teacher_replacement_schema):
    try:
        record = db.query(dbm.Teacher_Replacement_form).filter_by(
                teacher_tardy_reports_pk_id=Form.teacher_replacement_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.created_by_fk_id, Form.teacher_fk_id, Form.replacement_teacher_fk_id]):
            return 404, "Target Employee Not Found"
        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        record.created_by_fk_id = Form.created_by_fk_id
        record.teacher_fk_id = Form.teacher_fk_id
        record.replacement_teacher_fk_id = Form.replacement_teacher_fk_id
        record.class_fk_id = Form.class_fk_id
        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# business trip
def get_business_trip_form(db: Session, form_id):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(
                business_trip_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_business_trip_form(db: Session):
    try:
        data = db.query(dbm.Business_Trip_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_business_trip_form(db: Session, Form: sch.post_business_trip_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        OBJ = dbm.Business_Trip_form(
                employee_fk_id=Form.employee_fk_id,
                destination=Form.destination,
                description=Form.description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_business_trip_form(db: Session, form_id):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(
                business_trip_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_business_trip_form(db: Session, Form: sch.update_business_trip_schema):
    try:
        record = db.query(dbm.Business_Trip_form).filter_by(
                business_trip_pk_id=Form.business_trip_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        record.employee_fk_id = Form.employee_fk_id
        record.destination = Form.destination
        record.description = Form.description

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# class_cancellation
def get_class_cancellation_form(db: Session, form_id):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_class_cancellation_form(db: Session):
    try:
        data = db.query(dbm.Class_Cancellation_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_class_cancellation_form(db: Session, Form: sch.post_class_cancellation_schema):
    try:
        if not employee_exist(db, [Form.teacher_fk_id, Form.create_by_fk_id]):
            return 404, "Target Employee Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        OBJ = dbm.Class_Cancellation_form(
                create_by_fk_id=Form.create_by_fk_id,
                class_fk_id=Form.class_fk_id,
                teacher_fk_id=Form.teacher_fk_id,
                replacement=Form.replacement,
                class_duration=Form.class_duration,
                class_location=Form.class_location,
                description=Form.description,
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_class_cancellation_form(db: Session, form_id):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_class_cancellation_form(db: Session, Form: sch.update_class_cancellation_schema):
    try:
        record = db.query(dbm.Class_Cancellation_form).filter_by(
                class_cancellation_pk_id=Form.class_cancellation_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.teacher_fk_id, Form.create_by_fk_id]):
            return 404, "Target Employee Not Found"

        if not db.query(dbm.Class_form).filter_by(class_pk_id=Form.class_fk_id).first():
            return 404, "Target class Not Found"

        record.create_by_fk_id = Form.create_by_fk_id
        record.class_fk_id = Form.class_fk_id
        record.teacher_fk_id = Form.teacher_fk_id
        record.replacement = Form.replacement
        record.class_duration = Form.class_duration
        record.class_location = Form.class_location
        record.description = Form.description

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


# remote_request
def get_remote_request_form(db: Session, form_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=form_id,
                deleted=False
        ).first()
        if record:
            return 200, record
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_remote_request_form(db: Session):
    try:
        data = db.query(dbm.Remote_Request_form).filter_by(deleted=False).all()
        if data:
            return 200, data
        return 404, "Not Found"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_remote_request_form(db: Session, Form: sch.post_remote_request_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        OBJ = dbm.Remote_Request_form(
                employee_fk_id=Form.employee_fk_id,
                start_date=Form.start_date,
                end_date=Form.end_date,
                working_location=Form.working_location,
                description=Form.description
        )
        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_remote_request_form(db: Session, form_id):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        db.rollback()
        return 500, e.__repr__()


def update_remote_request_form(db: Session, Form: sch.update_remote_request_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(
                remote_request_pk_id=Form.remote_request_pk_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Not Found"

        if not employee_exist(db, [Form.employee_fk_id]):
            return 404, "Target Employee Not Found"

        record.employee_fk_id = Form.employee_fk_id,
        record.start_date = Form.start_date,
        record.end_date = Form.end_date,
        record.working_location = Form.working_location,
        record.description = Form.description

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logging.error(e)
        db.rollback()
        return 500, e.__repr__()
