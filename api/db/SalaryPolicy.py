from lib import logger
from sqlalchemy.orm import Session
import db.models as dbm
import schemas as sch
from .Extra import *


# SalaryPolicy_form
def get_SalaryPolicy(db: Session, form_id):
    try:
        return 200, db.query(dbm.SalaryPolicy_form).filter_by(SalaryPolicy_pk_id=form_id, deleted=False).first()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_SalaryPolicy(db: Session, page: sch.PositiveInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.SalaryPolicy_form, page, limit, order)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def report_SalaryPolicy(db: Session, Form: sch.salary_report):
    try:
        start, end = generate_month_interval(Form.year, Form.month)

        result = (
            db.query(dbm.SalaryPolicy_form)
            .filter_by(deleted=False, employee_fk_id=Form.employee_fk_id)
            .filter(dbm.SalaryPolicy_form.end_date.between(start, end))
            .all()
        )

        return 200, sum(row.duration for row in result)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_SalaryPolicy(db: Session, Form: sch.post_SalaryPolicy_schema):
    try:
        if not employee_exist(db, [Form.employee_fk_id, Form.created_fk_by]):
            return 400, "Bad Request: Employee Does Not Exist"

        data = Form.dict()

        if data["day_starting_time"] is None and data["Regular_hours_cap"] is None:
            return 400, "Bad Request: one of the following must have values: day_starting_time or Regular_hours_cap"

        if data["day_ending_time"] and data["day_starting_time"]:
            if Fix_time(data["day_ending_time"]) < Fix_time(data["day_starting_time"]):
                return 400, "Bad Request: End Date must be greater than Start Date"

        is_Fixed = True if data["day_starting_time"] and data["day_ending_time"] else False
        Working_hour = _sub(data["day_starting_time"], data["day_ending_time"]) if is_Fixed else data["Regular_hours_cap"]
        del data["Regular_hours_cap"]

        OBJ = dbm.SalaryPolicy_form(is_Fixed=is_Fixed, Regular_hours_cap=Working_hour, **data)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def delete_SalaryPolicy(db: Session, form_id):
    try:
        record = db.query(dbm.SalaryPolicy_form).filter_by(
                SalaryPolicy_pk_id=form_id,
                deleted=False
        ).first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def update_SalaryPolicy(db: Session, Form: sch.update_SalaryPolicy_schema):
    try:
        record = db.query(dbm.SalaryPolicy_form).filter_by(SalaryPolicy_pk_id=Form.SalaryPolicy_pk_id, deleted=False)
        if not record.first():
            return 404, "Record Not Found"

        if not employee_exist(db, [Form.employee_fk_id, Form.created_fk_by]):
            return 400, "Bad Request"
        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e.args}')
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'
