from lib import log

logger = log()
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import pandas as pd
import db.models as dbm
import schemas as sch
from .Extra import *
from fastapi import FastAPI, File, UploadFile, HTTPException

# Teacher Replacement
def get_fingerprint_scanner(db: Session, user_id):
    try:
        user = db.query(dbm.Employees_form).filter_by(employees_pk_id=user_id, deleted=False).first()
        if not user:
            return 400, "Bad Request"
        return 200, db.query(dbm.fingerprint_scanner_form).filter_by(user_ID=user.fingerprint_scanner_user_id, deleted=False).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def get_all_fingerprint_scanner(db: Session, page: int, limit: int):
    try:
        return 200, db.query(dbm.fingerprint_scanner_form).filter_by(deleted=False).offset((page - 1) * limit).limit(limit).all()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        # if not employee_exist(db, [Form.created_fk_by]):
        #     return 400, "Bad Request"

        OBJ = dbm.fingerprint_scanner_form(**Form.dict())

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()


def post_bulk_fingerprint_scanner(db: Session, file: UploadFile = File(...)):
    try:

        # if not employee_exist(db, [Form.created_fk_by]):
        #     return 400, "Bad Request"
        with open(f"./{file.filename}", "wb") as csv_file:
            csv_file.write(file.file.read())
        Data = pd.read_csv(f"./{file.filename}").to_dict(orient="records")
        OBJs = []
        for record in Data:
            del record["No"]
            record["In_Out"] = record.pop("In/Out")
            OBJs.append(dbm.fingerprint_scanner_form(**record))


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
        record = db.query(dbm.fingerprint_scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
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
        record = db.query(dbm.fingerprint_scanner_form).filter_by(teacher_tardy_reports_pk_id=Form.fingerprint_scanner_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by, Form.employee_fk_id]):
            return 400, "Bad Request"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, e.__repr__()
