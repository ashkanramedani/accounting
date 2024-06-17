import json
import uuid
from datetime import time, datetime
from typing import Dict, List

import pandas as pd
from sqlalchemy.orm import Session

import db.models as dbm
import schemas as sch
from lib import *
from .Salary_Utils import generate_daily_report, calculate_duration
from ..Extra import *
from uuid import UUID


# Teacher Replacement
def get_fingerprint_scanner(db: Session, form_id):
    try:
        return 200, db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_fingerprint_scanner(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: sch.Sort_Order = "desc"):
    try:

        return 200, record_order_by(db, dbm.Fingerprint_Scanner_form, page, limit, order)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_fingerprint_scanner(db: Session, EnNo: int | UUID, start_date, end_date):
    try:
        if isinstance(EnNo, UUID):
            User = db.query(dbm.User_form).filter_by(user_pk_id=EnNo, deleted=False).first()
            if not User:
                return 400, "Employee Nor Found"
            if not User.fingerprint_scanner_user_id:
                return 400, "Selected Employee Doesnt have FingerPrint scanner identifier. ( edit employee or provide EnNo Manually)"
            EnNo = User.fingerprint_scanner_user_id

        Fingerprint_scanner_report: List[dbm.Fingerprint_Scanner_form] = db.query(dbm.Fingerprint_Scanner_form) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start_date, end_date)) \
            .filter_by(deleted=False, EnNo=EnNo).all()

        if not Fingerprint_scanner_report:
            return 400, f"Employee Has No fingerprint record from {start_date} to {end_date}"
        return 200, Fingerprint_scanner_report

    except Exception as e:
        return Return_Exception(db, e)


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        # EnNo = db.query(dbm.User_form).filter_by(user_pk_id=data.pop("user_fk_id"), deleted=False).first().fingerprint_scanner_user_id
        User = db.query(dbm.User_form).filter_by(user_pk_id=data.pop("user_fk_id"), deleted=False).first()
        if not User:
            return 400, "Employee Not Found"
        if not User.fingerprint_scanner_user_id:
            return 400, "Selected Employee Doesnt have FingerPrint scanner identifier. ( edit employee or provide EnNo Manually)"
        EnNo = User.fingerprint_scanner_user_id

        if data["Enter"]:
            data["Enter"] = Fix_time(data["Enter"]).replace(second=0)
        if data["Exit"]:
            data["Exit"] = Fix_time(data["Exit"]).replace(second=0)

        Back_up_Body = {"created_fk_by": data["created_fk_by"], "TMNo": 0, "EnNo": EnNo, "GMNo": 0, "Mode": "Manually", "In_Out": "Normal", "Antipass": 0, "ProxyWork": 0}

        OBJs = [
            dbm.Fingerprint_Scanner_backup_form(**Back_up_Body, DateTime=f'{data["Date"]} {data["Enter"]}'),  # type: ignore[call-arg]
            dbm.Fingerprint_Scanner_backup_form(**Back_up_Body, DateTime=f'{data["Date"]} {data["Exit"]}'),  # type: ignore[call-arg]
            dbm.Fingerprint_Scanner_form(**data, duration=calculate_duration(data["Enter"], data["Exit"]))]  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def post_bulk_fingerprint_scanner(db: Session, created_fk_by: uuid.UUID, Data: pd.DataFrame):
    try:
        if not employee_exist(db, [created_fk_by]):
            return 400, "Bad Request: Employee Does Not Exist"

        start = datetime.combine(Data.iloc[0]["DateTime"], time())
        end = datetime.combine(Data.iloc[-1]["DateTime"] + pd.Timedelta(days=1), time())
        history_query = (
            db.query(dbm.Fingerprint_Scanner_backup_form.EnNo, dbm.Fingerprint_Scanner_backup_form.DateTime)
            .filter_by(deleted=False)
            .filter(dbm.Fingerprint_Scanner_backup_form.DateTime.between(start, end))
            .all()
        )
        Processed, total = 0, 0
        history = [f'{EnNo}{DateTime}' for EnNo, DateTime in history_query]
        Data = Data.to_dict(orient="records")
        OBJs, RES, ID = [], {}, {}

        if len(Data) == 0:
            logger.warning('400, "Empty File"')
            return 400, "Empty File"

        for record in Data:
            total += 1
            if f'{record["EnNo"]}{record["DateTime"]}' in history:
                continue

            Processed += 1
            OBJs.append(dbm.Fingerprint_Scanner_backup_form(created_fk_by=created_fk_by, **record))  # type: ignore[call-arg]
            record_time = record["DateTime"]
            EMP = record['EnNo']
            if EMP not in ID:
                ID[EMP] = record['EnNo']
            D, T = record_time.date(), record_time.time()
            if EMP not in RES:
                RES[EMP] = {}
            if D not in RES[EMP]:
                RES[EMP][D] = []
            RES[EMP][D].append(T)

        for EMP, Times in RES.items():
            for day, hour in Times.items():
                if len(hour) % 2:
                    hour.append(None)
                for H in range(0, len(hour), 2):
                    duration = calculate_duration(hour[H], hour[H + 1])
                    hour[H] = Fix_time(hour[H]) if hour[H] else None
                    hour[H + 1] = Fix_time(hour[H + 1]) if hour[H + 1] else None
                    OBJs.append(dbm.Fingerprint_Scanner_form(created_fk_by=created_fk_by, EnNo=EMP, Date=day, Enter=hour[H], Exit=hour[H + 1], duration=duration))  # type: ignore[call-arg]

        db.add_all(OBJs)
        db.commit()
        return 200, f"{Processed} from {total} record added"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_fingerprint_scanner(db: Session, form_id):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id, deleted=False).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=Form.fingerprint_scanner_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()

        s, e = data["Enter"], data["Exit"]
        data["duration"] = 0 if s == e else time_gap(Fix_time(s), Fix_time(s))

        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
