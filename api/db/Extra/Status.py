# from lib.decorators import DEV_io
from sqlalchemy.orm import Session

import models as dbm


def preprocess_keys(*args) -> list[str]:
    return [k.lower().strip() for k in args]


# @_io()
def Set_Status(db: Session, cluster: str, status: str) -> str:
    status, cluster = preprocess_keys(status, cluster)
    if status == "verified":
        status = "approved"

    Status_OBJ: dbm.Status_form = db.query(dbm.Status_form).filter_by(status_name=status, status_cluster=cluster).first()

    if not Status_OBJ:
        Status_OBJ = dbm.Status_form(status_name=status, status_cluster=cluster)  # type: ignore[call-arg]
        db.add(Status_OBJ)
        db.commit()
        db.refresh(Status_OBJ)
        return status

    return status
