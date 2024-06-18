import datetime
import os
import pathlib
from contextlib import asynccontextmanager
from json import dump
from time import sleep
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from redis import asyncio as redis
from sqlalchemy.exc import OperationalError

try:
    from db import models, save_route
    from router import routes
    from lib.log import logger
    from db.models import engine, SessionLocal
    from db import setUp_admin

except Exception as e:
    raise Exception(f"Error during importing libraries : f'{e.__class__.__name__}: {e.args}'")


@asynccontextmanager
async def app_lifespan(api: FastAPI):
    logger.info(f"Starting {api.title} -V: {api.version} - {datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=30)}")
    while True:
        try:
            # models.Base.metadata.drop_all(engine)
            models.Base.metadata.create_all(bind=engine)
            break
        except OperationalError as OE:
            logger.warning(f"[ Could Not Create Engine ]: {OE.__repr__()}")
            sleep(10)
    setUp_admin(SessionLocal())
    Redis_url = os.getenv('LOCAL_REDIS') if os.getenv('LOCAL_POSTGRES') else "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0"
    await FastAPILimiter.init(redis=redis.from_url(Redis_url, encoding="utf8"))
    yield
    logger.info(f"Shutting FastAPI - {datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=30)}")
    await FastAPILimiter.close()


app = FastAPI(swagger_ui_parameters={"docExpansion": "none"}, title="Accounting", version="0.1.0.0", lifespan=app_lifespan)

WHITELISTED_IPS: List[str] = []
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=["*"], allow_headers=["*"])

route_schema = save_route(routes)
dump(route_schema, open(f'{pathlib.Path(__file__).parent}/configs/routes.json', 'w'), indent=4)

for route in routes:
    app.include_router(route)
