import json

from lib import JSONEncoder
from models import tables as dbm

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.mapper import Mapper
def archive_deleted_record(mapper: Mapper, connection: Connection, target):
    ROW_DATA = target.__dict__
    ROW_DATA.pop("_sa_instance_state", None)

    value = next((key.replace("_pk_id", "") for key in ROW_DATA.keys() if "_pk_id" in key), None)

    with sessionmaker(autoflush=False, bind=connection)() as db:
        BackUp_Row = dbm.Deleted_Records(
                table=value,
                rows_data=json.loads(json.dumps(ROW_DATA, cls=JSONEncoder)),
                deleted_fk_by=ROW_DATA.pop("_Deleted_BY", None))

        db.add(BackUp_Row)
        db.commit()
        db.refresh(BackUp_Row)
