from datetime import datetime, date, timedelta
from typing import List, Any, Dict, Tuple
from uuid import UUID

from lib import logger
import models as dbm
from sqlalchemy import and_, func

# Assuming the models are defined as User, Role, and UsersRoles


from sqlalchemy.orm import Session

from pydantic import BaseModel

import pickle


def TestRoute(db: Session, created_by="00000000-0000-4b94-8e27-44833c2b940f", user_id="00000001-0000-4b94-8e27-44833c2b940f"):
    a = []
    for i in range(1, 5):
        for A, t in [(100, "fix")]:
            a.append(dbm.Reward_card_form(
                    start_date=date(2024, 1, i),
                    end_date=date(2024, 1, i) + timedelta(days=5),
                    reward_type=t,
                    user_fk_id=user_id,
                    created_fk_by=created_by,
                    reward_amount=A
            )
            )
    db.add_all(a)
    db.commit()
    db.flush()
    r = {}

    R: List = db.query(
            dbm.Reward_card_form.reward_type,
            func.sum(dbm.Reward_card_form.reward_amount).label("total_amount")
    ).filter(
            dbm.Reward_card_form.user_fk_id == user_id,
            and_(
                    dbm.Reward_card_form.start_date <= date(2024, 1, 2),
                    date(2024, 1, 2) <= dbm.Reward_card_form.end_date
            )
    ).group_by(
            dbm.Reward_card_form.reward_type
    ).all()
    return {r["reward_type"]: r["total_amount"] for r in R}


"""
SELECT
	course.course_type AS course_course_type,
	course.course_capacity AS course_course_capacity,
	course.course_level AS course_course_level,
	course_type_table.course_type_name AS course_type_table_course_type_name,
FROM
	course
	LEFT OUTER 
	JOIN course_type AS course_type_table 
	ON course_type_table.course_type_pk_id = course.course_type

"""
