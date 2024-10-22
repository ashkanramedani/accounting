import sys
from json import load
from os.path import normpath, dirname, join
from typing import Literal

from loguru import logger as logger_obj
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from loguru._defaults import *
from pytz import timezone

from lib import requester


def Time_formatter(time_record):
    return time_record.astimezone(tz=timezone("Iran")).strftime("%d-%m-%Y %H:%M:%S %Z")


def STDERR_FORMATTER(record):
    record["IR_time"] = Time_formatter(record["time"])

    Record = (" <y>{extra[name]: <6}</y> "
              " <g>{IR_time}</g> |"
              " <level>{level.no: <2}</level> |"
              " <c>{module}</c>:<c>{function}</c>:<c>{line}</c> |"
              " <level>{message}</level>\n")

    if record["extra"]["name"] == "Access":
        record["request_body"] = record["extra"].get("request_body", "Empty")
        record["response_body"] = record["extra"].get("response_body", "Empty")
        Record += (
            " >>> <y>request_body:</y><w> {request_body}</w>\n"
            " >>> <y>response_body:</y><w> {response_body}</w>\n"
        )

    return Record


OLD_LOG_PATH = "log/Log-{time:YYYY-MM}.jsonl"  # Deprecated
BASE_LOG_FILE = f'{normpath(f"{dirname(__file__)}/../log")}'


# filter = lambda record: record["level"].name != "INFO_access",
# self.logger.level("INFO_access", no=25, icon="✔️")


def FILE_FORMATTER(record):
    record["extra"]["serialized"] = {
        "timestamp": Time_formatter(record["time"]),
        "message": record["message"],
        "location": f'{record["module"]}:{record["function"]}:{record["line"]}',
        "level": record["level"].name,
        "file": record["file"].path,
    }
    return "{extra[serialized]}\n"


def ACCESS_FORMATTER(record):
    record["extra"]["serialized"] = {
        "timestamp": Time_formatter(record["time"]),
        "message": record["message"],
        "request_body": record["extra"]["request_body"],
        "response_body": record["extra"]["response_body"]}
    return "{extra[serialized]}\n"


class LOG:
    def __init__(self):
        self.Info_Status = [200, 201]
        self.Warn_Status = [400]
        self.ERR_Statis = [500]

        try:
            self.config_path = "configs/config.json"
        except FileNotFoundError:
            self.config_path = join(normpath(f'{dirname(__file__)}/../'), "configs/config.json")

        self.config = load(open(self.config_path))["logger"]
        self.developer = True

    def __getattr__(self, name):
        return getattr(logger_obj, name)

    def info(self, msg, depth=1):
        self.logger.opt(depth=depth).info(msg)

    def warning(self, msg, depth=1):
        self.logger.opt(depth=depth).warning(msg)

    def error(self, msg, depth=1):
        self.logger.opt(depth=depth).error(msg)

    def debug(self, msg, depth=1):
        self.logger.opt(depth=depth).debug(msg)


class Main_Log(LOG):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Main_Log, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.logger = _Logger(core=_Core(), exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})
            self.logger = self.logger.bind(name="Main")
            self.Main_Log_config = self.config["handler"]["Main"]

            self.log_level = self.Main_Log_config.pop("level", LOGURU_LEVEL)
            self.rotation = self.Main_Log_config.pop("rotation", None)
            self.compression = self.Main_Log_config.pop("compression", None)

            if self.Main_Log_config.pop("std_out", False):
                self.logger.add(sys.stdout, level=self.log_level, format=STDERR_FORMATTER)
            self.logger.add(f"{BASE_LOG_FILE}/{self.Main_Log_config.pop('file', 'Main_TMP.jsonl')}", level=self.log_level, format=FILE_FORMATTER, rotation=self.rotation, compression=self.compression)
            self._initialized = True

    def keep_log(self, msg, type_log, user_id, location):
        try:
            url = "logger_events"
            payload = {"username": user_id, "message": msg, "location": location, "typ": type_log}
            _obj_requester = requester.requester()
            _obj_requester.post(_url=url, payload=payload)

            self.show_log('keep_log', 's')

        except Exception as e:
            self.show_log(e, 'e')

    def show_log(self, msg, type_log):
        if self.developer and type_log == 'w':
            self.logger.opt(depth=1).warning(msg)
        if self.developer and type_log == 'd':
            self.logger.opt(depth=1).debug(msg)
        if type_log == 'e':
            self.logger.opt(depth=1).error(msg)
        if type_log == 's':
            self.logger.opt(depth=1).success(msg)
        if self.developer and type_log == 'i':
            self.logger.opt(depth=1).info(msg)

    def on_status_code(self, status_code, msg):
        if not isinstance(msg, str):
            msg = repr(msg)
        if status_code in self.Info_Status:
            self.logger.opt(depth=2).info(msg)
        elif status_code in self.Warn_Status:
            self.logger.opt(depth=2).warning(msg)
        elif status_code in self.ERR_Statis:
            self.logger.opt(depth=2).error(msg)
        else:
            self.logger.opt(depth=2).warning("Status Code Has Not Beet Categorised.\n\t{msg}")


class Access_Log(LOG):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Access_Log, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self.logger = _Logger(core=_Core(), exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})
            self.logger = self.logger.bind(name="Access")
            self.Main_Log_config = self.config["handler"]["Access"]

            self.log_level = self.Main_Log_config.pop("level", LOGURU_LEVEL)
            self.rotation = self.Main_Log_config.pop("rotation", None)
            self.compression = self.Main_Log_config.pop("compression", None)

            if self.Main_Log_config.pop("std_out", False):
                self.logger.add(sys.stdout, level=self.log_level, format=STDERR_FORMATTER)

            self.logger.add(f"{BASE_LOG_FILE}/{self.Main_Log_config.pop('file', 'Access_TMP.jsonl')}", level=self.log_level, format=ACCESS_FORMATTER, rotation=self.rotation, compression=self.compression)
            self._initialized = True

    def info(self, msg, depth=1, **Binds):
        self.logger.opt(depth=depth).bind(**Binds).info(msg)


logger = Main_Log()
access_log = Access_Log()

if __name__ == '__main__':
    logger.info('test')
