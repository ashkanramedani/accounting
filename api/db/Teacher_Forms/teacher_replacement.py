from sqlalchemy import and_

from lib import logger

from sqlalchemy.orm import Session, joinedload

import db.models as dbm
import schemas as sch
from ..Extra import *


# Teacher Replacement


def session_teacher_replacement(db: Session, Form: sch.session_teacher_replacement):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.sub_teacher_fk_id]):
            return 400, "Bad Request"

        if not db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.sub_course_fk_id, deleted=False).first():
            return 400, "Bad Request: subcourse not found"

        sub_course = db.query(dbm.Session_form).filter_by(sub_course_fk_id=Form.sub_course_fk_id, subcourse_pk_id=Form.session_fk_id, deleted=False).all()
        sub_course_id = [i.session_pk_id for i in sub_course]

        data = Form.dict()
        sessions = data.pop("session_fk_id")

        if any(i not in sub_course_id for i in sessions):
            return 400, "Bad Request: Session not found"

        new_sessions = []
        for session_id in sessions:
            tmp_session_object = db.query(dbm.Session_form).filter_by(session_pk_id=session_id, deleted=False)
            old_session = tmp_session_object.first()

            tmp_session_object_data = old_session.dict()
            tmp_session_object_data.update({"is_sub": True, "session_teacher_fk_id": Form.sub_teacher_fk_id})

            new_sessions.append(dbm.Session_form(**tmp_session_object_data))  # type: ignore[call-arg]
            tmp_session_object.update({"deleted": True})

        db.add_all(new_sessions)
        db.commit()
        return 200, "Record has been Added"

    except Exception as e:
        logger.error(e)
        db.rollback()
        return 500, f'{e.__class__.__name__}: {e.args}'



def sub_course_teacher_replacement(db: Session, Form: sch.subcourse_teacher_replacement):
    try:
        if not employee_exist(db, [Form.created_fk_by, Form.sub_teacher_fk_id]):
            return 400, "Bad Request"

        if not db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.subcourse_fk_id, deleted=False).first():
            return 400, "Bad Request: subcourse not found"

        NotStarted = db.query(dbm.Session_form).filter_by(sub_course_fk_id=Form.subcourse_fk_id, deleted=False).filter(dbm.Session_form.session_starting_time.between(Form.start_date, Form.end_date)).count()

        replacement_date = Fix_datetime(Form.replacement_date)

        records = (
            db.query(dbm.Session_form)
            .filter_by(sub_course_fk_id=Form.subcourse_fk_id, deleted=False)
            .filter(dbm.Session_form.session_starting_time > (replacement_date.time()))
            .all()
        )
        records = (
            db.query(dbm.Session_form)
            .filter_by(sub_course_fk_id=Form.subcourse_fk_id, deleted=False)
            .filter(and_(
                    dbm.Session_form.session_starting_time > (replacement_date.time()),
                    dbm.Session_form.session_date >= replacement_date.date(),
                    dbm.Session_form.session_date > replacement_date.time()
            ))
            .all()
        )

        # data = Form.dict()
        # replacement_date = Fix_datetime(data.pop("replacement_date"))
        # if any(i not in sessions for i in Form.session_fk_id):
        #     return 400, "Bad Request: Session not found"
        #
        # new_sessions = []
        # for session_id in sessions:
        #     tmp_session_object = db.query(dbm.Session_form).filter_by(session_pk_id=session_id, deleted=False)
        #     old_session = tmp_session_object.first()
        #
        #     tmp_session_object_data = old_session.dict()
        #     tmp_session_object_data.update({"is_sub": True, "session_teacher_fk_id": Form.sub_teacher_fk_id})
        #
        #     new_sessions.append(dbm.Session_form(**tmp_session_object_data))  # type: ignore[call-arg]
        #     tmp_session_object.update({"deleted": True})
        #
        # db.add_all(new_sessions)
        # db.commit()
        return 200, "Record has been Added"
    except Exception:
        pass