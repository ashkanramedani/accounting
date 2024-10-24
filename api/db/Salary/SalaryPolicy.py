from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from lib import time_gap
from ..Extra import *


# Salary_Policy_form
def get_SalaryPolicy(db: Session, form_id):
    try:
        return 200, db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=form_id).filter(dbm.Salary_Policy_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_SalaryPolicy(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Salary_Policy_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_SalaryPolicy(db: Session, Form: sch.post_SalaryPolicy_schema):
    try:
        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request: Employee Does Not Exist"

        data = Form.dict()
        # "Fixed" "Split" "Hourly"
        if Form.Salary_Type == "Fixed":
            start, end = data["day_starting_time"], data["day_ending_time"]
            if not start or not end:
                return 400, "Bad Request: one of the following Doesn't have values: (day_starting_time, day_ending_time)"

            start, end = Fix_time(start), Fix_time(end)
            if end < start:
                return 400, "Bad Request: End Date must be greater than Start Date"

            data["Regular_hours_cap"] = time_gap(start, end)

        elif Form.Salary_Type == "Hourly" or Form.Salary_Type == "Split":
            if not data["Regular_hours_cap"]:
                return 400, "Bad Request: Regular_hours_cap is required"
        else:
            return 400, "Bad Request: Invalid Salary Type"

        OBJ = dbm.Salary_Policy_form(**data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_SalaryPolicy(db: Session, form_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=form_id).filter(dbm.Salary_Policy_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_SalaryPolicy(db: Session, Form: sch.update_SalaryPolicy_schema):
    try:
        record = db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=Form.salary_policy_pk_id).filter(dbm.Salary_Policy_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_SalaryPolicy_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=form_id).first()
        if not record:
            return 400, "Record Not Found"

        status = db.query(dbm.Status_form).filter_by(status_pk_id=status_id).first()
        if not status:
            return 400, "Status Not Found"

        db.add(dbm.Status_history(status=record.status, table_name=record.__tablename__))
        record.status = status.status_name
        db.commit()

        return 200, "Status Updated"
    except Exception as e:
        return Return_Exception(db, e)
