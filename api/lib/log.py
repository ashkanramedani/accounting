from loguru import logger
from .requester import requester
from .json_handler import json_handler

class log():
    def __init__(self, config={}):
        if config == {}:
            # self._obj_json_handler = json_handler(FilePath="config.json")     
            self.developer = True #self._obj_json_handler.Data['developer_log']
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
            logger.warning(msg)
        if self.developer and type_log == 'd':
            logger.debug(msg)
        if type_log == 'e':
            logger.error(msg)
        if type_log == 's':
            logger.success(msg)
        if  self.developer and type_log == 'i':
            logger.info(msg)
   
    def log(self, msg, type_log, user, location, keep=False):
        self.show_log(msg, type_log)
        if keep:
            self.keep_log(msg, type_log, user, location)
       