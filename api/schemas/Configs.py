from enum import Enum
from pydantic import BaseModel, constr

IP_PATTERN = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"


class DatabaseType(str, Enum):
    POSTGRESQL = 'postgresql'


class Engine(BaseModel):
    echo: bool
    pool_recycle: int


class Setting(BaseModel):
    database_type: DatabaseType
    ip: constr(regex=IP_PATTERN)
    port: int
    username: str
    password: str
    database: str
    engine: Engine
