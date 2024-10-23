import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, no_type_check
from uuid import UUID
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, Integer
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


def FK_Column(table: str, unique: bool = False, index: bool = True, nullable: bool = False, name=None):
    table_name = table.lower().replace("_form", "")
    if name:
        return Column(name, GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}'), nullable=nullable, unique=unique, index=index)
    return Column(GUID, ForeignKey(f'{table_name}.{table_name + "_pk_id"}'), nullable=nullable, unique=unique, index=index)


def FKA_Column(fk: str, pk: str):
    return Column(fk, GUID, ForeignKey(pk), nullable=False, unique=False, index=True)


def association_table(base, *tables, field: str = None):
    if len(tables) < 2:
        raise ValueError("At least two tables are required to create an association table.")

    tables = sorted({table.lower().replace('_form', '') for table in tables})
    FKA_Columns = (FKA_Column(fk, pk) for fk, pk in [(f'{table}_fk_id', f'{table}.{table}_pk_id') for table in tables])

    return Table(f'{"_".join(tables)}{("_" + field if field else "")}_Association', base.metadata, *FKA_Columns, UniqueConstraint(*(f'{table}_fk_id' for table in tables)))


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
