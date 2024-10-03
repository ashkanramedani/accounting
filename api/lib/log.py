import sys
from json import load
from os.path import normpath, dirname, join

from loguru import logger as logger_obj
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from pytz import timezone

from lib import requester

STDERR_FORMATTER = " <green>{time:YYYY-MM-DD HH:mm:ss Z}</green> | <level>{level.no: <2}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
OLD_LOG_PATH = "log/Log-{time:YYYY-MM}.jsonl"
BASE_LOG_FILE = f'{normpath(f"{dirname(__file__)}/../log")}'


# filter = lambda record: record["level"].name != "INFO_access",
# self.logger.level("INFO_access", no=25, icon="✔️")

def Time_formatter(time_record):
    return time_record.astimezone(tz=timezone("Iran")).strftime("%d-%m-%Y %H:%M:%S %Z")


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
    record["extra"]["serialized"] = {"timestamp": Time_formatter(record["time"]), "message": record["message"], "data": record["extra"]["data"]}
    return "{extra[serialized]}\n"


class LOG:
    def __init__(self):
        self.Info_Status = [200, 201]
        self.Warn_Status = [400]
        self.ERR_Statis = [500]

        try:
            self.config_path = "configs/config.json"
            self.config = load(open(self.config_path))["logger"]
        except FileNotFoundError:
            self.config_path = join(normpath(f'{dirname(__file__)}/../'), "configs/config.json")
            self.config = load(open(self.config_path))["logger"]

        self.developer = True

        self.log_level = self.config.pop("level", 20)
        self.rotation = self.config.pop("rotation", "1 MB")
        self.compression = self.config.pop("compression", "zip")
        self.logger = _Logger(core=_Core(), exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})

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
            self.logger.add(sys.stdout, level=self.log_level, format=STDERR_FORMATTER)
            self.logger.add(f"{BASE_LOG_FILE}/Api_Log.jsonl", level=self.log_level, format=FILE_FORMATTER, rotation=self.rotation, compression=self.compression)
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
            self.logger.add(f"{BASE_LOG_FILE}/Api_access.jsonl", format=ACCESS_FORMATTER, rotation=self.rotation, compression=self.compression)
            self._initialized = True

    def info(self, msg, depth=1, **Binds):
        self.logger.opt(depth=depth).bind(**Binds).info(msg)


logger = Main_Log()
access_log = Access_Log()

if __name__ == '__main__':
    logger.info('test')
