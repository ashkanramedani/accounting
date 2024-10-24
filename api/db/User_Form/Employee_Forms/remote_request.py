from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *
from lib import Separate_days


# remote_request
def get_remote_request_form(db: Session, form_id):
    try:
        return 200, db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=form_id).filter(dbm.Remote_Request_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_remote_request_form(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Remote_Request_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def report_remote_request(db: Session, user_fk_id, start_date, end_date):
    try:
        Remote_Request_report = db.query(dbm.Remote_Request_form) \
            .filter_by(user_fk_id=user_fk_id) \
            .filter(dbm.Remote_Request_form.date.between(start_date, end_date), dbm.Remote_Request_form.status != "deleted") \
            .all()

        return 200, Remote_Request_report
    except Exception as e:
        return Return_Exception(db, e)


def post_remote_request_form(db: Session, Form: sch.post_remote_request_schema):
    try:
        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request: Employee not found"

        data = Form.dict()
        Start, End = Fix_datetime(data.pop("start_date")), Fix_datetime(data.pop("end_date"))

        if End < Start:
            return 400, "Bad Request: End Date must be greater than Start Date"
        OBJs = []
        for Day in Separate_days(Start, End):
            OBJs.append(dbm.Remote_Request_form(**Day, **data))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_remote_request_form(db: Session, form_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=form_id).filter(dbm.Remote_Request_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_remote_request_form(db: Session, Form: sch.update_remote_request_schema):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=Form.remote_request_pk_id).filter(dbm.Remote_Request_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def Verify_remote_request(db: Session, Form: sch.Verify_remote_request_schema, status: sch.CanUpdateStatus):
    try:
        Warn = []
        verified = 0
        records = db.query(dbm.Remote_Request_form) \
            .filter(dbm.Remote_Request_form.deleted == False, dbm.Remote_Request_form.status != "deleted", dbm.Remote_Request_form.status != status, dbm.Remote_Request_form.remote_request_pk_id.in_(Form.remote_request_id)) \
            .all()

        for record in records:
            record.status = Set_Status(db, "form", status)
            verified += 1

        db.commit()
        if Warn:
            return 200, f"{verified} Form Update Status To {status}. {' | '.join(Warn)}"
        return 200, f"{len(records)} Form Update Status To {status}."
    except Exception as e:
        return Return_Exception(db, e)


def update_remote_request_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Remote_Request_form).filter_by(remote_request_pk_id=form_id).first()
        if not record:
            return 404, "Form Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
