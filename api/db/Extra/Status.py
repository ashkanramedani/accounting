from sqlalchemy.orm import Session

import db.models as dbm


def preprocess_keys(*args):
    return [k.lower().strip() for k in args]


def Set_Status(db: Session, cluster: str, status: str) -> str:
    status, cluster = preprocess_keys(status, cluster)

    Status_OBJ: dbm.Status_form = db.query(dbm.Status_form).filter_by(status_name=status, status_cluster=cluster).first()

    if not Status_OBJ:
        try:
            Admin = db.query(dbm.User_form).filter_by(name="Admin", last_name="Admin").first().user_pk_id
        except AttributeError:
            raise AttributeError("Admin User Not Found")
        Status_OBJ = dbm.Status_form(status_name=status, status_cluster=cluster, created_fk_by=Admin)  # type: ignore[call-arg]
        db.add(Status_OBJ)
        db.commit()
        db.refresh(Status_OBJ)
        return status

    return Status_OBJ.status_name
