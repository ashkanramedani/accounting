from sqlalchemy.orm import Session

import models as dbm
import schemas as sch
from ..Extra import *


def get_tag(db: Session, tag_id):
    try:
        return 200, db.query(dbm.Tag_form).filter_by(tag_pk_id=tag_id).filter(dbm.Tag_form.status != "deleted").first()

    except Exception as e:
        return Return_Exception(db, e)


def get_all_tag(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Tag_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_tag(db: Session, Form: sch.post_tag_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Employee Not Found"
        OBJ = dbm.Tag_form(**Form.dict())  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)
        return 200, " Tag Created"

    except Exception as e:
        return Return_Exception(db, e)


def delete_tag(db: Session, tag_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Tag_form).filter_by(tag_pk_id=tag_id).filter(dbm.Tag_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()

        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_tag(db: Session, Form: sch.update_tag_schema):
    try:
        record = db.query(dbm.Tag_form).filter_by(tag_pk_id=Form.tag_pk_id).filter(dbm.Tag_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)

def update_tag_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Tag_form).filter_by(tag_pk_id=form_id).first()
        if not record.first():
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


def get_category(db: Session, category_id):
    try:
        return 200, db.query(dbm.Category_form).filter_by(category_pk_id=category_id).filter(dbm.Category_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_category(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Category_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_category(db: Session, Form: sch.post_category_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Employee Not Found"

        OBJ = dbm.Category_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, f'category Added. ID: {OBJ.category_pk_id}'
    except Exception as e:
        return Return_Exception(db, e)


def delete_category(db: Session, category_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Category_form).filter_by(category_pk_id=category_id).filter(dbm.Category_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_category(db: Session, Form: sch.update_category_schema):
    try:
        record = db.query(dbm.Category_form).filter_by(category_pk_id=Form.category_pk_id).filter(dbm.Category_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)


def update_category_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Category_form).filter_by(category_pk_id=form_id).first()
        if not record.first():
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

def get_language(db: Session, language_id):
    try:
        return 200, db.query(dbm.Language_form).filter_by(language_pk_id=language_id).filter(dbm.Language_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_language(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Language_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_language(db: Session, Form: sch.post_language_schema):
    try:

        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Employee Not Found"

        OBJ = dbm.Language_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, f'language Added'
    except Exception as e:
        return Return_Exception(db, e)


def delete_language(db: Session, language_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Language_form).filter_by(language_pk_id=language_id).filter(dbm.Language_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_language(db: Session, Form: sch.update_language_schema):
    try:
        record = db.query(dbm.Language_form).filter_by(language_pk_id=Form.language_pk_id).filter(dbm.Language_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)

def update_language_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Language_form).filter_by(language_pk_id=form_id).first()
        if not record.first():
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

def get_course_type(db: Session, course_type_id):
    try:
        return 200, db.query(dbm.Course_Type_form).filter_by(course_type_pk_id=course_type_id).filter(dbm.Course_Type_form.status != "deleted").first()
    except Exception as e:
        return Return_Exception(db, e)


def get_all_course_type(db: Session, page: sch.NonNegativeInt, limit: sch.PositiveInt, order: str = "desc", SortKey: str = None):
    try:
        return record_order_by(db, dbm.Course_Type_form, page, limit, order, SortKey)
    except Exception as e:
        return Return_Exception(db, e)


def post_course_type(db: Session, Form: sch.post_course_type_schema):
    try:
        if not employee_exist(db, [Form.created_fk_by]):
            return 400, "Employee Not Found"
        OBJ = dbm.Course_Type_form(**Form.__dict__)  # type: ignore[call-arg]

        db.add(OBJ)
        db.commit()
        db.refresh(OBJ)

        return 200, f'course_type Added'
    except Exception as e:
        return Return_Exception(db, e)


def delete_course_type(db: Session, course_type_id, deleted_by: UUID = None):
    try:
        record = db.query(dbm.Course_Type_form).filter_by(course_type_pk_id=course_type_id).filter(dbm.Course_Type_form.status != "deleted").first()
        if not record:
            return 404, "Record Not Found"
        record._Deleted_BY = deleted_by
        db.delete(record)
        db.commit()
        return 200, "Deleted"
    except Exception as e:
        return Return_Exception(db, e)


def update_course_type(db: Session, Form: sch.update_course_type_schema):
    try:
        record = db.query(dbm.Course_Type_form).filter_by(course_type_pk_id=Form.course_type_pk_id).filter(dbm.Course_Type_form.status != "deleted")
        if not record.first():
            return 404, "Record Not Found"

        record.update(Form.dict(), synchronize_session=False)

        db.commit()
        return 200, "Record Updated"
    except Exception as e:
        return Return_Exception(db, e)

def update_course_type_status(db: Session, form_id: UUID, status_id: UUID):
    try:
        record = db.query(dbm.Course_Type_form).filter_by(course_type_pk_id=form_id).first()
        if not record.first():
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
