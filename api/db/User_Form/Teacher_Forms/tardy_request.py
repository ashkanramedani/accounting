from sqlalchemy.orm import Session, joinedload

import schemas as sch
from db import models as dbm
from db.Extra import *
from lib import logger


# Tardy Form - get_tardy_request
def get_tardy_request(db: Session, form_id):
    try:
        return 200, db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_reports_pk_id=form_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").first()
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def get_all_tardy_request(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc"):
    try:
        return 200, record_order_by(db, dbm.Teacher_Tardy_report_form, page, limit, order)
    except Exception as e:
        return Return_Exception(db, e)


@not_implemented
def report_tardy_request(db: Session, Form: sch.teacher_report):
    try:
        result = (
            db.query(dbm.Teacher_Tardy_report_form)
            .join(dbm.Course_form, dbm.Course_form.course_pk_id == dbm.Teacher_Tardy_report_form.course_fk_id)
            .filter_by(teacher_fk_id=Form.teacher_fk_id)
            .filter(dbm.Course_form.course_time.between(Form.start_date, Form.end_date), dbm.Teacher_Tardy_report_form.status != "deleted")
            .options(joinedload(dbm.Teacher_Tardy_report_form.course))
            .all()
        )

        return 200, sum(row.delay for row in result)
    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'


def post_tardy_request(db: Session, Form: sch.post_teacher_tardy_reports_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request: Employee Not Found"
        if not db.query(dbm.Sub_Course_form).filter_by(course_fk_id=Form.course_fk_id, sub_course_pk_id=Form.sub_course_fk_id, sub_course_teacher_fk_id=Form.teacher_fk_id).filter(dbm.Sub_Course_form.status != "deleted").first():
            return 400, "Bad Request: subcourse with given course and teacher not found"

        OBJ = dbm.Teacher_Tardy_report_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, "Record has been Added"
    except Exception as e:
        return Return_Exception(db, e)


def delete_tardy_request(db: Session, form_id):
    try:
        record = db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_reports_pk_id=form_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record.deleted = True
        record.status = Set_Status(db, "form", "deleted")
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_tardy_request(db: Session, Form: sch.update_teacher_tardy_reports_schema):
    try:
        record = db.query(dbm.Teacher_Tardy_report_form).filter_by(teacher_tardy_reports_pk_id=Form.teacher_tardy_reports_pk_id).filter(dbm.Teacher_Tardy_report_form.status != "deleted")

        if not employee_exist(db, [Form.created_fk_by, Form.teacher_fk_id]):
            return 400, "Bad Request"

        if not db.query(dbm.Course_form).filter_by(course_pk_id=Form.course_fk_id).filter(dbm.Course_form.status != "deleted").first():
            return 400, "Bad Request: course not found"
        if not db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id).filter(dbm.Sub_Course_form.status != "deleted").first():
            return 400, "Bad Request: subcourse not found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Form Updated"
    except Exception as e:
        return Return_Exception(db, e)
