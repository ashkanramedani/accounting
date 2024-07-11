import json

from dotenv import load_dotenv

try:
    from os import getenv
    from time import sleep
    from typing import List
    from pathlib import Path
    from json import dump, load
    from datetime import datetime, timedelta, timezone

    # DB
    from redis import asyncio as redis
    from sqlalchemy.exc import OperationalError

    # fastApi
    from fastapi import FastAPI
    from fastapi_limiter import FastAPILimiter
    from contextlib import asynccontextmanager
    from fastapi.middleware.cors import CORSMiddleware

except (ImportError, ModuleNotFoundError):
    raise Exception('Requirement Not Satisfied: some_module is missing')

from lib import logger, JSONEncoder
from router import routes
from db import models, save_route, setUp_admin, engine, SessionLocal, Create_Redis_URL
import schemas

config = load(open("configs/config.json"))


@asynccontextmanager
async def app_lifespan(api: FastAPI):
    try:
        logger.info(f"Starting {api.title} V: {api.version} - {datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3, minutes=30)}")
        while True:
            try:
                # models.Base.metadata.drop_all(engine)
                models.Base.metadata.create_all(bind=engine)
                break
            except OperationalError as OE:
                logger.warning(f"[ Could Not Create Engine ]: {OE.__repr__()}")
                sleep(10)
        with SessionLocal() as db:
            setUp_admin(db)

        await FastAPILimiter.init(redis=redis.from_url(Create_Redis_URL(), encoding="utf8"))
        yield
    except KeyboardInterrupt:
        logger.info(f'Exited')
    logger.info(f"Shutting FastAPI - {datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3, minutes=30)}")
    await FastAPILimiter.close()

load_dotenv()
app = FastAPI(
        lifespan=app_lifespan,
        version=config["versions"],
        swagger_ui_parameters={"docExpansion": "none"},
        title=getenv('ACC_NAME') if getenv('ACC_NAME') else config["title"],
        debug=getenv('SWAGGER_DEBUG') if getenv('SWAGGER_DEBUG') else config["debug"])

WHITELISTED_IPS: List[str] = []
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=["*"], allow_headers=["*"])

route_schema = save_route(routes)
dump(route_schema, open(f'{Path(__file__).parent}/configs/routes.json', 'w'), indent=4)

for route in routes:
    app.include_router(route)
