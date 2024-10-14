import json

from sqlalchemy.exc import StatementError

from lib import JSONEncoder, logger
from models import tables as dbm

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.mapper import Mapper


def archive_deleted_record(mapper: Mapper, connection: Connection, target):
    """
        ROW_DATA should not be modify it can effect deleting process
    """
    try:
        Fields = {}
        ROW_DATA = target.__dict__
        ROW_DATA.pop("_sa_instance_state", None)
        value = next((key for key in ROW_DATA.keys() if "_pk_id" in key), None)

        Fields["table"] = value.replace("_pk_id", "")
        Fields["rows_data"] = json.loads(json.dumps(ROW_DATA, cls=JSONEncoder))
        if Deleted_by := ROW_DATA.pop("_Deleted_BY", None):
            Fields["deleted_fk_by"] = Deleted_by
        with sessionmaker(autoflush=False, bind=connection)() as db:
            BackUp_Row = dbm.Deleted_Records(**Fields)
            db.add(BackUp_Row)
            db.commit()
            db.refresh(BackUp_Row)

    except StatementError as SE:
        logger.error(f'{SE.__class__.__name__}: {SE.__repr__()}')
