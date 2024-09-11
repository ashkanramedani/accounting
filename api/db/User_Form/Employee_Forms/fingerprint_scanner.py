import uuid
from datetime import time, datetime
from typing import List

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from db.Extra import *
from lib import *
from lib.decorators import DEV_io
from .Salary_Utils import calculate_duration


# Teacher Replacement
def get_fingerprint_scanner(db: Session, form_id):
    try:
        return 200, db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id).filter(dbm.Fingerprint_Scanner_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_fingerprint_scanner(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: sch.Sort_Order = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Fingerprint_Scanner_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


@DEV_io()
def report_fingerprint_scanner(db: Session, EnNo: int | UUID, start_date, end_date):
    try:
        if isinstance(EnNo, UUID):
            User = db.query(dbm.User_form).filter_by(user_pk_id=EnNo).filter(dbm.User_form.status != "deleted").first()
            if not User:
                return 400, "Employee Not Found"
            if not User.fingerprint_scanner_user_id:
                return 400, "Selected Employee Doesnt have FingerPrint scanner identifier. ( edit employee or provide EnNo Manually)"
            EnNo = User.fingerprint_scanner_user_id

        FingerScanner_Query = db \
            .query(dbm.Fingerprint_Scanner_form) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start_date, end_date)) \
            .filter_by(EnNo=EnNo) \
            .filter(dbm.Fingerprint_Scanner_form.status != "deleted")

        Report: List = FingerScanner_Query.order_by(dbm.Fingerprint_Scanner_form.Date).all()

        TotalHour = db \
            .query(func.sum(dbm.Fingerprint_Scanner_form.duration).label("Duration")) \
            .filter(dbm.Fingerprint_Scanner_form.Date.between(start_date, end_date)) \
            .filter_by(valid=True, EnNo=EnNo) \
            .first().Duration

        if not Report:
            return 400, f"Employee Has No fingerprint record from {start_date} to {end_date}"

        return 200, {
            "Fingerprint_scanner_report": Report,
            "Invalid": FingerScanner_Query.filter_by(valid=False).count(),
            "TotalHour": TotalHour}

    except Exception as e:
        return Return_Exception(db, e)


def post_fingerprint_scanner(db: Session, Form: sch.post_fingerprint_scanner_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        # EnNo = db.query(dbm.User_form).filter_by(user_pk_id=data.pop("user_fk_id")).filter(dbm.User_form.status != "deleted").first().fingerprint_scanner_user_id
        User = db.query(dbm.User_form).filter_by(user_pk_id=data.pop("user_fk_id")).filter(dbm.User_form.status != "deleted").first()
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
            dbm.Fingerprint_Scanner_form(**data, EnNo=EnNo, duration=calculate_duration(data["Enter"], data["Exit"]))]  # type: ignore[call-arg]

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
            .filter(dbm.Fingerprint_Scanner_backup_form.status != "deleted")
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
        return Return_Exception(db, e)


def delete_fingerprint_scanner(db: Session, form_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id).filter(dbm.Fingerprint_Scanner_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_fingerprint_scanner(db: Session, Form: sch.update_fingerprint_scanner_schema):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=Form.fingerprint_scanner_pk_id).filter(dbm.Fingerprint_Scanner_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()

        # EnNo = db.query(dbm.User_form).filter_by(user_pk_id=data.pop("user_fk_id")).filter(dbm.User_form.status != "deleted").first().fingerprint_scanner_user_id
        # data["EnNo"] = EnNo
        s, e = data["Enter"], data["Exit"]
        data["duration"] = 0 if s == e else time_gap(Fix_time(s), Fix_time(e))

        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)

def update_fingerprint_scanner_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Fingerprint_Scanner_form).filter_by(fingerprint_scanner_pk_id=form_id).first()
        if not record:
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.update({"status": status.status_name}, synchronize_session=False)
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
