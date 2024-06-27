from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

import json
import os
from os.path import dirname, normpath
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationError
from sqlalchemy import create_engine

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

    logger.info(SQLALCHEMY_DATABASE_URL)
    return create_engine(SQLALCHEMY_DATABASE_URL, **DB_config["engine"])


engine = Create_engine()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
