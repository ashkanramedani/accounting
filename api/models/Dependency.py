# Dependency
from sqlalchemy.orm import Session, sessionmaker
from models import Create_engine


class Engine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Create_engine()
        return cls._instance


engine = Engine()
SESSION = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Session:
    db = SESSION()
    try:
        yield db
    finally:
        db.close()
