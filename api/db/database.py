from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import os
from loguru import logger
from lib.json_handler import json_handler
from lib.log import log


#to get the current working directory
directory = os.getcwd()
_obj_json_handler_config = json_handler(FilePath=directory +"/configs/config.json")
config =  _obj_json_handler_config.Data
_obj_log = log()
logger.add(sink=os.path.join(os.path.dirname(__file__), config["logger"]["file"]["path"]), rotation=config["logger"]["file"]["size"], format=config["logger"]["format"], level="INFO")

if config['developer']:
    SQLALCHEMY_DATABASE_URL = f"{config['db_test']['database_type']}://{config['db_test']['username']}{':' if config['db_test']['username'] != '' else ''}{config['db_test']['password']}{'@' if config['db_test']['username'] != '' else ''}{config['db_test']['ip']}:{config['db_test']['port']}/{config['db_test']['database_name']}"
else:
    SQLALCHEMY_DATABASE_URL = f"{config['db']['database_type']}://{config['db']['username']}:{config['db']['password']}@{config['db']['ip']}:{config['db']['port']}/{config['db']['database_name']}"

if config['developer_log']:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600)

if config['developer_log']:
    _obj_log.show_log(SQLALCHEMY_DATABASE_URL, 'i')
    
# engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
