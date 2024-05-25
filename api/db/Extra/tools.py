import functools
from functools import wraps
# from faker import Faker
from typing import Tuple

from lib import logger


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


MESSAGE = {
    501: "Not Implemented",
    503: "Service Unavailable",
    400: "Bad Request",
    403: "Forbidden"
}


def NOT_AVAILABLE(status_code: int, message: str | None = None):
    message = message if message else MESSAGE[status_code]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return status_code, message

        return wrapper

    return decorator


def safe_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
        return func(*args, **kwargs)

    return wrapper
