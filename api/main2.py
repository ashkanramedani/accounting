import os
import pathlib
import datetime
from contextlib import asynccontextmanager

from time import sleep
from typing import List
from json import load, dump
from fastapi import FastAPI
from redis import asyncio as redis
from fastapi_limiter import FastAPILimiter
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware

from db import models
from router import routes
from lib.log import logger
from db.models import engine, SessionLocal
from db import setUp_admin

db = SessionLocal()
# Ensure you import the necessary modules
from sqlalchemy.orm import joinedload

# Proper query to avoid Cartesian product
query = db.query(models.User_form).options(joinedload(models.User_form.Teacher_tardy_reports_Relation)).all()
for user in query:
    print(user.__dict__)