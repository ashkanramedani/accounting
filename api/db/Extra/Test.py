# Assuming the models are defined as User, Role, and UsersRoles


from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, joinedload

import models as dbm
from ..Extra import *

from lib import logger


def TestRoute(db: Session, role: str):
    return
