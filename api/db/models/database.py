import json
import os
from os.path import dirname, normpath
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from lib import logger
from schemas import Setting

load_dotenv()
directory = normpath(f'{dirname(__file__)}/../../configs/config.json')
DB_config = json.load(open(directory)).get("db", {})


def is_valid_setting(setting_data: dict) -> tuple[bool, Any]:
    try:
        Setting(**setting_data)
        return True, ""
    except (ValidationError, ValueError) as e:
        return False, e


def Postgres_URL(**kwargs) -> str:
    is_Valid, msg = is_valid_setting(kwargs)
    if is_Valid:
        return f"{kwargs['database_type']}://{kwargs['username']}:{kwargs['password']}@{kwargs['ip']}:{kwargs['port']}/{kwargs['database']}"
    else:
        raise Exception(msg)


if os.getenv('LOCAL_POSTGRES'):
    SQLALCHEMY_DATABASE_URL = os.getenv('LOCAL_POSTGRES')
else:
    SQLALCHEMY_DATABASE_URL = Postgres_URL(**DB_config)

engine = create_engine(SQLALCHEMY_DATABASE_URL, **DB_config["engine"])
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

logger.info(SQLALCHEMY_DATABASE_URL)


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
