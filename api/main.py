try:
    from os import getenv
    from time import sleep
    from typing import List
    from pathlib import Path
    from json import dump, load
    from dotenv import load_dotenv
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

from router import routes
from lib import logger
from db import models, save_route, SetUp, engine, SessionLocal, Create_Redis_URL

config = load(open("configs/config.json"))


@asynccontextmanager
async def app_lifespan(api):
    try:
        logger.info(f"preparing {api.title} V: {api.version} - {datetime.now()}")
        while True:
            try:
                # models.Base.metadata.drop_all(engine)
                models.Base.metadata.create_all(bind=engine)
                break
            except OperationalError as OE:
                logger.warning(f"[ Could Not Create Engine ]: {OE.__repr__()}")
                sleep(10)
        with SessionLocal() as db:
            SetUp(db)

        await FastAPILimiter.init(redis=redis.from_url(Create_Redis_URL(), encoding="utf8"))
        logger.info(f'{api.title} V: {api.version} Has been started ...')
        yield

    except KeyboardInterrupt:
        logger.info(f'Exited')
    logger.info(f'Exiting from {api.title} V: {api.version} - {datetime.now()}')
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

if getenv('CREATE_ROUTE_SCHEMA'):
    route_schema = save_route(routes)
    dump(route_schema, open(f'{Path(__file__).parent}/configs/routes.json', 'w'), indent=4)

for route in routes:
    app.include_router(route)
