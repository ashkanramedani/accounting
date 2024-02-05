from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os.path import dirname, normpath, join
from loguru import logger
from lib import json_handler, log

directory = normpath(f'{dirname(__file__)}/../configs/config.json')
_obj_json_handler_config = json_handler(FilePath=directory)
config = _obj_json_handler_config.Data
_obj_log = log()
logger.add(
        sink=join(dirname(__file__), config["logger"]["file"]["path"]),
        rotation=config["logger"]["file"]["size"],
        format=config["logger"]["format"],
        level="INFO")

if config['developer']:
    SQLALCHEMY_DATABASE_URL = f"{config['db_test']['database_type']}://{config['db_test']['username']}{':' if config['db_test']['username'] != '' else ''}{config['db_test']['password']}{'@' if config['db_test']['username'] != '' else ''}{config['db_test']['ip']}:{config['db_test']['port']}/{config['db_test']['database_name']}"
else:
    SQLALCHEMY_DATABASE_URL = f"{config['db']['database_type']}://{config['db']['username']}:{config['db']['password']}@{config['db']['ip']}:{config['db']['port']}/{config['db']['database_name']}"

SQLALCHEMY_DATABASE_URL = "postgresql://admin:adminadmin@localhost:5432/tmp5"


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
