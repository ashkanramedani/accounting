import json
from os import getenv
from os.path import dirname, normpath
from typing import Dict

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from lib import logger
from schemas import Setting


def Create_engine(DB_config: Dict = None):
    try:
        if not DB_config:
            load_dotenv()
            if getenv('CONFIG_PATH'):
                DB_config = json.load(open(getenv('CONFIG_PATH'))).get("db", {})
            else:
                directory = normpath(f'{dirname(__file__)}/../configs/config.json')
                DB_config = json.load(open(directory)).get("db", {})

        logger.info("Creating engine ...")

        Setting.construct(**DB_config)
        SQLALCHEMY_DATABASE_URL = f"{DB_config['target_DB']}://{DB_config['username']}:{DB_config['password']}@{DB_config['ip']}:{DB_config['port']}/{DB_config['database']}"

        logger.info(f'Postgres: {SQLALCHEMY_DATABASE_URL}')
        return create_engine(SQLALCHEMY_DATABASE_URL, **DB_config["engine"])
    except Exception as e:
        logger.error(e.__repr__())



def Create_Redis_URL(Config):
    if not Config:
        logger.error("Redis config not found.")
        return None
    Redis_url = f"redis://:{Config['password']}@{Config['host']}:{Config['port']}/{Config['db']}"
    logger.info(f'Redis: {Redis_url}')
    return Redis_url


# Dependency
def get_db() -> Session:
    db = sessionmaker(autoflush=False, bind=Create_engine())()
    try:
        yield db
    finally:
        db.close()
