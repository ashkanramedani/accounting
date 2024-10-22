import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, no_type_check
from uuid import UUID

from fastapi_utils.guid_type import GUID_SERVER_DEFAULT_POSTGRESQL as UNIQUE_ID, UUIDTypeDecorator, GUID as GTYPE
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import CHAR

BASE_ATTR = [
    "created_fk_by",
    "_sa_instance_state",
    "priority",
    "visible",
    "deleted",
    "can_update",
    "can_deleted",
    "create_date",
    "update_date",
    "expire_date",
    "status",
    "description",
    "note"]

CODES = {
    "user": "0",
    "role": "1",
    "status": "2",
    "language": "3",
    "course_type": "4"
}


class GUID(GTYPE):
    cache_ok = True


from sqlalchemy import BigInteger


def create_OLD_id():
    return Column(BigInteger, nullable=True, unique=True, index=True)


def create_Unique_ID():
    return Column(GUID, server_default=UNIQUE_ID, primary_key=True, nullable=False, unique=True, index=True)


def create_foreignKey(table: str, unique: bool = False, index: bool = True, nullable: bool = False):
    table_name = table.lower().replace("_form", "")
    return Column(GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}'), nullable=nullable, unique=unique, index=index)


def Remove_Base_Data(OBJ) -> str:
    for i in BASE_ATTR:
        OBJ.pop(i, None)
    return repr(OBJ)


def IRAN_TIME(dump: bool = False):
    if dump:
        return str(datetime.now(tz=timezone(offset=timedelta(hours=3, minutes=30))))
    return datetime.now(tz=timezone(offset=timedelta(hours=3, minutes=30)))


def Extract_Unique_keyPair(error_message) -> str | Dict:
    error_message = str(error_message)
    match = re.search(r'Key \((.*?)\)=\((.*?)\)', error_message)
    if match:
        return ', '.join([f'{k} -> {v}' for k, v in zip(match.group(1).split(', '), match.group(2).split(', '))]).replace('"', '')
    else:
        return error_message


def Unique_ID(num: int, code: str) -> str:
    return f"{str(num).zfill(8)}-{CODES.get(code, 0).zfill(4)}-4b94-8e27-44833c2b940f"
