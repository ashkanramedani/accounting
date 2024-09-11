# Dependency
from sqlalchemy.orm import Session, sessionmaker

from models import Create_engine
engine = Create_engine()
SESSION = sessionmaker(autoflush=False, bind=engine)

def get_db() -> Session:
    db = SESSION()
    try:
        yield db
    finally:
        db.close()
