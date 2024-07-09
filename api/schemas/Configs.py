from enum import Enum

from pydantic import BaseModel, constr

IPV4_PATTERN = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"


class DB(str, Enum):
    POSTGRESQL = 'postgresql'


class Engine(BaseModel):
    echo: bool
    pool_recycle: int


class Setting(BaseModel):
    target_DB: DB
    ip: constr(regex=IPV4_PATTERN)
    port: int
    username: str
    password: str
    database: str
    engine: Engine
