import json
import os
from os import getenv
from os.path import dirname, normpath
from typing import Any

import sqlalchemy
from dotenv import load_dotenv
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import DeclarativeBase

from lib import logger
from schemas import Setting


def is_valid_setting(setting_data: dict) -> tuple[bool, Any]:
    try:
        Setting(**setting_data)
        return True, ""
    except (ValidationError, ValueError) as e:
        return False, e


def Postgres_URL(**kwargs) -> str:
    is_Valid, msg = is_valid_setting(kwargs)
    if is_Valid:
        return f"{kwargs['target_DB']}://{kwargs['username']}:{kwargs['password']}@{kwargs['ip']}:{kwargs['port']}/{kwargs['database']}"
    else:
        raise Exception(msg)


def Create_engine():
    load_dotenv()
    directory = normpath(f'{dirname(__file__)}/../../configs/config.json')
    DB_config = json.load(open(directory)).get("db", {})

    if os.getenv('LOCAL_POSTGRES'):
        SQLALCHEMY_DATABASE_URL = os.getenv('LOCAL_POSTGRES')
    else:
        SQLALCHEMY_DATABASE_URL = Postgres_URL(**DB_config)

    logger.info(f'Postgres: {SQLALCHEMY_DATABASE_URL}')
    return create_engine(SQLALCHEMY_DATABASE_URL, **DB_config["engine"])


def Create_Redis_URL() -> str:
    load_dotenv()
    directory = normpath(f'{dirname(__file__)}/../../configs/config.json')
    Config = json.load(open(directory)).get("redis", {})

    if getenv('LOCAL_REDIS'):
        Redis_url = getenv('LOCAL_REDIS')
    else:
        Redis_url = f"redis://:{Config['password']}@{Config['host']}:{Config['port']}/{Config['db']}"
    logger.info(f'Redis: {Redis_url}')
    return Redis_url


engine = Create_engine()
SessionLocal = sessionmaker(autoflush=False, bind=engine)


if sqlalchemy.__version__ >= "2.0":
    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):  # new approch since SqlAlchemy 2.0
        pass

else:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()  # changed due to SqlAlchemy 2.0 update




# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
