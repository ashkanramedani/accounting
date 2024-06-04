from lib import logger, generate_month_interval, Fix_time, time_gap

from sqlalchemy.orm import Session
import db.models as dbm
import schemas as sch
from ..Extra import *


# Salary_Policy_form
def get_SalaryPolicy(db: Session, form_id):
    try:
        return 200, db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=form_id, deleted=False).first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_SalaryPolicy(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Salary_Policy_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


def report_SalaryPolicy(db: Session, Form: sch.salary_report):
    try:
        start, end = generate_month_interval(Form.year, Form.month)

        result = (
            db.query(dbm.Salary_Policy_form)
            .filter_by(deleted=False, user_fk_id=Form.user_fk_id)
            .filter(dbm.Salary_Policy_form.end_date.between(start, end))
            .all()
        )

        return 200, sum(row.duration for row in result)

    except Exception as e:
        return Return_Exception(db, e)


def post_SalaryPolicy(db: Session, Form: sch.post_SalaryPolicy_schema):
    try:
        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request: Employee Does Not Exist"

        data = Form.dict()

        if data["day_starting_time"] is None and data["Regular_hours_cap"] is None:
            return 400, "Bad Request: one of the following must have values: day_starting_time or Regular_hours_cap"

        if data["day_ending_time"] and data["day_starting_time"]:
            if Fix_time(data["day_ending_time"]) < Fix_time(data["day_starting_time"]):
                return 400, "Bad Request: End Date must be greater than Start Date"

        del data["Regular_hours_cap"]

        if data["undertime_factor"] > 0:
            data["undertime_factor"] *= -1

        OBJ = dbm.Salary_Policy_form(Regular_hours_cap=Working_hour, **data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_SalaryPolicy(db: Session, form_id):
    try:
        record = db.query(dbm.Salary_Policy_form).filter_by(
                salary_policy_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_SalaryPolicy(db: Session, Form: sch.update_SalaryPolicy_schema):
    try:
        record = db.query(dbm.Salary_Policy_form).filter_by(salary_policy_pk_id=Form.salary_policy_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"


        if not employee_exist(db, [Form.user_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"

        data = Form.dict()
        if data["undertime_factor"] > 0:
            data["undertime_factor"] *= -1
        record.update(data, synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)
