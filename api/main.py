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
from db import setUp_admin

try:
    PRJ_file = str(pathlib.Path(__file__).parent.resolve())
    abs_config = os.path.join(PRJ_file, "configs/config.json")
    config = load(open(abs_config))
    if "abs_sink" not in config["logger"]:
        config["logger"]["abs_sink"] = ""

    config["logger"]["abs_sink"] = f'{PRJ_file}/{config["logger"]["sink"]}'
    dump(config, open(abs_config, 'w'), indent=4)

    from db import models
    from router import routes
    from lib.log import logger
    from db.models import engine, SessionLocal

    logger.info("Logger Configured")

except Exception as e:
    raise Exception(f"Error during importing libraries : f'{e.__class__.__name__}: {e.args}'")


@asynccontextmanager
async def app_lifespan(api: FastAPI):
    logger.info(f"Starting FastAPI - {datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=30)}")
    while True:
        try:
            # models.Base.metadata.drop_all(engine)
            models.Base.metadata.create_all(bind=engine)
            break
        except OperationalError as e:
            logger.warning(f"[ Could Not Create Engine ]: {e.__repr__()}")
            sleep(10)
    setUp_admin(SessionLocal())
    Redis_url = os.getenv('LOCAL_REDIS') if os.getenv('LOCAL_POSTGRES') else "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0"
    await FastAPILimiter.init(redis=redis.from_url(Redis_url, encoding="utf8"))
    yield
    logger.info(f"Shutting FastAPI - {datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=30)}")
    dump(config, open(abs_config, 'w'), indent=4)
    await FastAPILimiter.close()


app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"},
        title="Accounting",
        lifespan=app_lifespan)

WHITELISTED_IPS: List[str] = []
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
)


Rotes_Schema = {}
for route in routes:
    tag = route.tags.__str__().replace("['", "").replace("']", "")
    Rotes_Schema[tag] = {}
    for route_signature in route.routes:
        methods = route_signature.methods.__str__().replace("{'", "").replace("'}", "")
        if methods not in Rotes_Schema[tag]:
            Rotes_Schema[tag][methods] = []
        url = route_signature.path.split("{")[0] + "<UUID>" if "{" in route_signature.path else route_signature.path
        Rotes_Schema[tag][methods].append(f"http://localhost:5001{url}")
    app.include_router(route)


dump(Rotes_Schema, open(f'{PRJ_file}/configs/routes.json', 'w'), indent=4)
