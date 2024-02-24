import redis
from loguru import logger


class Redis:
    def __init__(self, config: dict) -> None:
        self.show_report = config["show_report"]
        self.connection_id = config["connection_id"]
        self.pool = None
        self.redis_conn = None
        self.connection_name = "" if self.connection_id == -1 else f"[{self.connection_id}] "
        self.report = ""
        try:
            self.pool = redis.ConnectionPool(host=config["host"], port=config["port"], db=config["db"], password=config["password"])
            self.redis_conn = redis.Redis(connection_pool=self.pool, decode_responses=config["decode_responses"])
        except Exception as error:
            self.redis_conn = None
            if self.show_report:
                logger.error(error)

    def key_exists(self, key: str) -> bool:
        try:
            if self.redis_conn.exists(key):
                return True
        except Exception as e:
            if self.show_report:
                logger.error(e)
        return False

    def set_key(self, key: str, value: str = "", ttl_time: int = 0) -> bool:
        try:
            if self.redis_conn.setex(name=key, value=value, time=ttl_time):
                return True
            return False
        except Exception as error:
            if self.show_report:
                logger.error(error)
        return False

    def get_key(self, key: str) -> str:
        val = self.redis_conn.get(name=key)
        if val:
            return val.decode("utf-8")

        raise ValueError(f"the key does not exist. given key : {key}")

    def remove_key(self, key: str) -> None:
        if self.key_exists(key=key):
            self.redis_conn.delete(key)
            return
        raise ValueError(f"the key does not exist. given key : {key}")

    def close_connection(self) -> None:
        try:
            self.redis_conn.connection_pool.disconnect()
            return
        except Exception as e:
            if self.show_report:
                logger.error(e)

# configs={
#             "host": "87.107.161.173",
#             "port": 6379,
#             "password": "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324",
#             "db": 5,
#             "decode_responses": True,
#             "show_report": True,
#             "connection_id": -1
#         }
# _obj_redis = Redis(configs)

# _obj_redis.set_key("1:1",1,24*60*60)