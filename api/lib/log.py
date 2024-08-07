import sys
from json import load
from os.path import normpath, dirname, join

from loguru import logger as logger_obj

from lib import requester


class Log:
    def __init__(self):
        self.Info_Status = [200, 201]
        self.Warn_Status = [400]
        self.ERR_Statis = [500]

        try:
            self.config_path = "configs/config.json"
            config = load(open(self.config_path))
        except FileNotFoundError:
            self.config_path = join(normpath(f'{dirname(__file__)}/../'), "configs/config.json")
            config = load(open(self.config_path))

        self.developer = True
        self.logger = logger_obj
        self.logger.remove()

        self.logger.add("log/Log-{time:YYYY-MM-DD}.log", **config["logger"])
        self.logger.add(sys.stdout, level=config["logger"]["level"])
        self.logger.info(f" ------------ Logger OBJ created ------------ ")

    @property
    def log_path(self):
        return "log/Log-[Date].log"

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

    def log(self, msg, type_log, user, location, keep=False):
        self.show_log(msg, type_log)
        if keep:
            self.keep_log(msg, type_log, user, location)

    def info(self, msg, depth=1):
        self.logger.opt(depth=depth).info(msg)

    def warning(self, msg, depth=1):
        self.logger.opt(depth=depth).warning(msg)

    def error(self, msg, depth=1):
        self.logger.opt(depth=depth).error(msg)

    def debug(self, msg, depth=1):
        self.logger.opt(depth=depth).debug(msg)

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


logger = Log()

if __name__ == '__main__':
    logger.info('test')
