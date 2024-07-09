from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

import schemas as sch
from db import models as dbm
from db.Extra import *


# Teacher Replacement

def preprocess_old_session(session):
    for filed in ["_sa_instance_state", "is_sub", "session_teacher_fk_id", "session_pk_id"]:
        if filed in session:
            session.pop(filed)
    return session


def sub_course_teacher_replacement(db: Session, Form: sch.subcourse_teacher_replacement):
    try:
        if not employee_exist(db, [Form.sub_teacher_fk_id]):
            return 400, "Bad Request"

        if not db.query(dbm.Sub_Course_form).filter_by(sub_course_pk_id=Form.subcourse_fk_id).filter(dbm.Sub_Course_form.status != "deleted").first():
            return 400, "Bad Request: subcourse not found"

        replacement_date = Fix_datetime(Form.replacement_date)

        All_sub_course_sessions = db.query(dbm.Session_form).filter_by(sub_course_fk_id=Form.subcourse_fk_id).filter(dbm.Session_form.status != "deleted")
        Not_Started_session = (
            db.query(dbm.Session_form)
            .filter_by(sub_course_fk_id=Form.subcourse_fk_id).filter(dbm.Session_form.status != "deleted")
            .filter(
                    or_(
                            dbm.Session_form.session_date > replacement_date.date(),
                            and_(
                                    dbm.Session_form.session_date == replacement_date.date(),
                                    dbm.Session_form.session_starting_time >= replacement_date.time()
                            )
                    )
            )
            .all()
        )

        new_sessions = []
        for session_data in [{k: v for k, v in session.__dict__.items() if k != "_sa_instance_state" and "_pk_" not in k} for session in Not_Started_session]:
            session_data = preprocess_old_session(session_data)

            new_Session = dbm.Session_form(**session_data, is_sub=True, session_teacher_fk_id=Form.sub_teacher_fk_id)  # type: ignore[call-arg]
            new_sessions.append(new_Session)

        db.add_all(new_sessions)
        All_sub_course_sessions.update({"deleted": True})
        db.commit()
        return 200, "Session teacher has been update"
    except Exception as e:
        return Return_Exception(db, e)
