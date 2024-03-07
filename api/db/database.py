import os
from os.path import dirname, normpath

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from lib.json_handler import json_handler
from lib.log import log

# to get the current working directory
load_dotenv()
directory = normpath(f'{dirname(__file__)}/../configs/config.json')
_obj_json_handler_config = json_handler(FilePath=directory)
config = _obj_json_handler_config.Data
_obj_log = log()

if config['developer']:
    SQLALCHEMY_DATABASE_URL = f"{config['db_test']['database_type']}://{config['db_test']['username']}{':' if config['db_test']['username'] != '' else ''}{config['db_test']['password']}{'@' if config['db_test']['username'] != '' else ''}{config['db_test']['ip']}:{config['db_test']['port']}/{config['db_test']['database_name']}"
else:
    SQLALCHEMY_DATABASE_URL = f"{config['db']['database_type']}://{config['db']['username']}:{config['db']['password']}@{config['db']['ip']}:{config['db']['port']}/{config['db']['database_name']}"

if config['developer']:
    SQLALCHEMY_DATABASE_URL = f"{config['db_test']['database_type']}://{config['db_test']['username']}{':' if config['db_test']['username'] != '' else ''}{config['db_test']['password']}{'@' if config['db_test']['username'] != '' else ''}{config['db_test']['ip']}:{config['db_test']['port']}/{config['db_test']['database_name']}"
else:
    SQLALCHEMY_DATABASE_URL = f"{config['db']['database_type']}://{config['db']['username']}:{config['db']['password']}@{config['db']['ip']}:{config['db']['port']}/{config['db']['database_name']}"

if os.getenv('LOCAL_POSTGRES'):
    SQLALCHEMY_DATABASE_URL = os.getenv('LOCAL_POSTGRES')

if config['developer_log']:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
    _obj_log.show_log(SQLALCHEMY_DATABASE_URL, 'i')
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
