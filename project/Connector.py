from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from json import load

Config = load(open("./Config.json", 'r'))
engine = create_engine(Config["DB"]["Address"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PSQL = declarative_base()




