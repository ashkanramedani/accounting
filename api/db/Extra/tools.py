import functools
from functools import wraps
# from faker import Faker
from typing import Tuple, List

import fastapi

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


def get_attr(Obj):
    Res = {}
    for atr in dir(Obj):
        try:
            Value = str(getattr(Obj, atr))
        except AttributeError:
            Value = str(atr)

        Res[atr] = Value
    return Res


def save_route(routes):
    Rotes_Schema = {}
    for route in routes:
        try:
            tag = f'{route.tags}'[2:-2] if route.tags else "[]"
            if tag not in Rotes_Schema:
                Rotes_Schema[tag] = []
            for route_signature in route.routes:
                methods = f'{route_signature.methods}'[2:-2]
                url = route_signature.path
                # url = route_signature.path.split("{")[0] + "<UUID>" if "{" in route_signature.path else route_signature.path
                FullURL = f'[{methods: <6}] {url}'
                if FullURL not in Rotes_Schema[tag]:
                    Rotes_Schema[tag].append(FullURL)
        except AttributeError:
            continue
    return Rotes_Schema


def save_route2(routes: List[fastapi.APIRouter]) -> dict:
    def prepare_inner_dict(sub_route):
        return {
            "url": sub_route.path,
            "method": f'{sub_route.methods}'[2:-2],
            "params": str(getattr(getattr(sub_route, "endpoint"), "__annotations__"))
        }

    Rotes_Schema = {}
    for route in routes:
        try:
            tag = f'{route.tags}'[2:-2] if route.tags else "[]"
            if tag in Rotes_Schema:
                continue
            Rotes_Schema[tag] = [prepare_inner_dict(route_signature) for route_signature in route.routes]
        except Exception as e:
            logger.error(e)
    return Rotes_Schema
