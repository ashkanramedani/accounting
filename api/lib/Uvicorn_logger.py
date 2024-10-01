import http
import logging
from copy import copy


class DefaultFormatter(logging.Formatter):
    def __init__(self, fmt: str = None, datefmt: str = None):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def formatMessage(self, record: logging.LogRecord) -> str:
        record_copy = copy(record)
        record_copy.__dict__["levelprefix"] = f'{record_copy.levelname: <{8 - len(record_copy.levelname)}}'
        return super().formatMessage(record_copy)


def get_status_code(status_code: int) -> str:
    try:
        status_phrase = http.HTTPStatus(status_code).phrase
    except ValueError:
        status_phrase = ""
    return f"{status_code} {status_phrase}"


class AccessFormatter(logging.Formatter):
    def __init__(self, fmt: str = None, datefmt: str = None):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def formatMessage(self, record: logging.LogRecord) -> str:
        return super().formatMessage(record)
        # record_copy = copy(record)
        # r = record_copy.__dict__
        # print(r)
        # client_addr, method, full_path, http_version, status_code = record_copy.args
        # status_code = get_status_code(int(status_code))
        # record_copy.__dict__.update({"client_addr": client_addr, "request_line": f"{method} {full_path}", "status_code": status_code})

        # record_copy.__dict__.update({})


class StatReloadFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        try:
            if "StatReload detected changes" in record.message:
                return False
            return True
        except AttributeError:
            return True
