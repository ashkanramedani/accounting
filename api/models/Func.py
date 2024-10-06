import functools
import re
from collections.abc import Callable
from lib import logger
from typing import Dict
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


CODES = {
    "user": "0",
    "role": "1",
    "status": "2",
    "language": "3",
    "course_type": "4"
}


def Exception_Wrapper(func: Callable):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'{func.__name__} - {args} - {kwargs}')
        try:
            func(*args, **kwargs)
        except Exception as Error:
            return
            db = kwargs["db"]
            Cluster = func.__name__
            db.rollback()
            if "duplicate key" in Error.__repr__() or "UniqueViolation" in Error.__repr__():
                logger.warning(f'[ {Cluster} / 409 ]{Error.__class__.__name__}: Record Already Exist: {Extract_Unique_keyPair(Error.args)}', depth=2)
                return
            logger.error(f'[ {Cluster} / 500 ]{Error.__class__.__name__}: {Error.args}', depth=2)

    return wrapper()

def Unique_ID(num: int, code: str) -> str:
    return f"{str(num).zfill(8)}-{CODES.get(code, 0).zfill(4)}-4b94-8e27-44833c2b940f"
