from fastapi_utils.guid_type import GUID as GUID_TYPE, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, ForeignKey
from datetime import datetime, timedelta, timezone

BASE_ATTR = ["created_fk_by", "_sa_instance_state", "priority", "visible", "deleted", "can_update", "can_deleted", "create_date", "update_date", "delete_date", "expire_date", "status", "description", "note"]


class GUID(GUID_TYPE):
    cache_ok = True


def create_Unique_ID():
    return Column(
            GUID,
            server_default=GUID_SERVER_DEFAULT_POSTGRESQL,
            primary_key=True,
            nullable=False,
            unique=True,
            index=True)


def create_foreignKey(table: str, unique: bool = False, index: bool = True, nullable: bool = False):
    table_name = table.lower().replace("_form", "")
    return Column(GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}'), nullable=nullable, unique=unique, index=index)


def Remove_Base_Data(OBJ) -> str:
    for i in BASE_ATTR:
        OBJ.pop(i, None)
    return repr(OBJ)


def IRAN_TIME():
    return datetime.now(tz=timezone(offset=timedelta(hours=3, minutes=30)))
