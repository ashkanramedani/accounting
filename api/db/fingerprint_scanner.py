import uuid

from fastapi import File, UploadFile

from lib import logger


from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import pandas as pd
import db.models as dbm
import schemas as sch
from .Extra import *


# Teacher Replacement
def get_fingerprint_scanner(db: Session, user_id):
    try:
        user = db.query(dbm.Employees_form).filter_by(employees_pk_id=user_id, deleted=False).first()
        if not user:
            return 400, "Bad Request"
        return 200, db.query(dbm.Fingerprint_scanner_form).filter_by(user_ID=user.fingerprint_scanner_user_id, deleted=False).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_fingerprint_scanner(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: sch.Sort_Order = "desc"):
    try:
        return 200, record_order_by(db, dbm.Fingerprint_scanner_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        OBJ = dbm.Fingerprint_scanner_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_bulk_fingerprint_scanner(db: Session, created_fk_by: uuid.UUID, file: UploadFile = File(...)):
    try:
        if not employee_exist(db, [created_fk_by]):
            return 400, "Bad Request"

        with open(f"./{file.filename}", "wb") as csv_file:
            csv_file.write(file.file.read())
        Data = pd.read_csv(f"./{file.filename}").to_dict(orient="records")
        OBJs, RES, ID = [], {}, {}

        for record in Data:
            time = record["DateTime"]
            EMP = record['Name']
            if EMP not in ID:
                ID[EMP] = record['EnNo']
            D, T = time.split(" ")
            if EMP not in RES:
                RES[EMP] = {}
            if D not in RES[EMP]:
                RES[EMP][D] = []
            RES[EMP][D].append(T)

        for EMP, timming in RES.items():
            for day, hour in timming.items():
                if len(hour) % 2:
                    hour.append(None)
                for H in range(0, len(hour), 2):
                    OBJs.append(dbm.Fingerprint_scanner_form(created_fk_by=created_fk_by, EnNo=ID[EMP], Name=EMP, Date=day, Enter=hour[H], Exit=hour[H+1]))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "File added"

    except IntegrityError:
        db.rollback()
        return 409, "UniqueViolation"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.Fingerprint_scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.Fingerprint_scanner_form).filter_by(teacher_tardy_reports_pk_id=Form.fingerprint_scanner_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


"""
def post_bulk_fingerprint_scanner(db: Session, Form: sch.post_bulk_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"
        with open(f"./{Form.file.filename}", "wb") as csv_file:
            csv_file.write(Form.file.file.read())
        Data = pd.read_csv(f"./{Form.file.filename}").to_dict(orient="records")
        OBJs = []
        for record in Data:
            del record["No"]
            record["In_Out"] = record.pop("In/Out")
            OBJs.append(dbm.Fingerprint_scanner_form(created_fk_by=Form.created_fk_by, **record))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "File added"

    except IntegrityError:
        db.rollback()
        return 409, "UniqueViolation"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()

"""