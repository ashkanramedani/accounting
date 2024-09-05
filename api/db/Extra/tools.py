import functools
from functools import wraps
# from faker import Faker
from typing import Tuple

from lib import logger


def prepare_param(key, val):
    table = key.lower().replace("_fk_id", "").replace("_pk_id", "")
    if key in ["created", "session_main_teacher", "session_sub_teacher", "employee", "teacher", "employees"]:
        table = "employee"
    elif table not in Tables:
        return None, table
    return Tables[table], {"deleted": False, key.replace("_fk_id", "_pk_id"): val}

def log_on_status(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[int, str]:
        status, message = func(*args, **kwargs)
        logger.on_status_code(status, message)
        return status, message

    return wrapper


def not_implemented(func):
    def wrapper(*args, **kwargs):
        return 501, "Not Implemented"
    return wrapper

def out_of_service(func):
  def wrapper(*args, **kwargs):
    return 503, "Service Unavailable"
  return wrapper


def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        return func(*args, **kwargs)

    return wrapper