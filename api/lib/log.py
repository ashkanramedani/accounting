from os.path import normpath, dirname, join

from loguru import logger as L
from lib.requester import requester
from json import load


class log:
    def __init__(self, config: dict = None):
        self.logger = L
        if not config:
            self.developer = True
            PRJ_path = normpath(f'{dirname(__file__)}/../')
            config = load(open(join(PRJ_path, "configs/config.json"), 'r'))["logger"]
            config["sink"] = join(PRJ_path, config["sink"])

        else:
            self.developer = config['developer_log']


    def keep_log(self, msg, type_log, user_id, location):
        try:
            url = "logger_events"
            payload = {
                "username": user_id,
                "message": msg,
                "location": location,
                "typ": type_log
            }
            _obj_requester = requester()
            _obj_requester.post( _url=url, payload=payload)

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
        if  self.developer and type_log == 'i':
            self.logger.opt(depth=1).info(msg)
   
    def log(self, msg, type_log, user, location, keep=False):
        self.show_log(msg, type_log)
        if keep:
            self.keep_log(msg, type_log, user, location)

    def info(self, msg):
        self.logger.opt(depth=1).info(msg)
    def warning(self, msg):
        self.logger.opt(depth=1).warning(msg)

    def error(self, msg):
        self.logger.opt(depth=1).error(msg)

if __name__ == '__main__':
    Logger = log()
    Logger.info("INFO")
    Logger.error("ERROR")
    Logger.warning("WARNING")
