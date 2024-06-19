try:
    from json import dump
    from os import getenv
    from time import sleep
    from typing import List
    from pathlib import Path
    from datetime import datetime, timedelta, timezone

    from redis import asyncio as redis
    from sqlalchemy.exc import OperationalError

    from fastapi import FastAPI
    from fastapi_limiter import FastAPILimiter
    from contextlib import asynccontextmanager
    from fastapi.middleware.cors import CORSMiddleware

except (ImportError, ModuleNotFoundError):
    raise Exception('Requirement Not Satisfied: some_module is missing')

try:
    from lib import logger
    from router import routes
    from db import models, save_route, setUp_admin, engine, SessionLocal

except Exception as e:
    raise Exception(f"Error during importing libraries : f'{e.__class__.__name__}: {e.args}'")


@asynccontextmanager
async def app_lifespan(api: FastAPI):
    try:
        logger.info(f"Starting {api.title} -V: {api.version} - {datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3, minutes=30)}")
        while True:
            try:
                # models.Base.metadata.drop_all(engine)
                models.Base.metadata.create_all(bind=engine)
                break
            except OperationalError as OE:
                logger.warning(f"[ Could Not Create Engine ]: {OE.__repr__()}")
                sleep(10)
        setUp_admin(SessionLocal())
        Redis_url = getenv('LOCAL_REDIS') if getenv('LOCAL_POSTGRES') else "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0"
        await FastAPILimiter.init(redis=redis.from_url(Redis_url, encoding="utf8"))
        yield
    except KeyboardInterrupt:
        logger.info(f'Exited')
    finally:
        logger.info(f"Shutting FastAPI - {datetime.now(timezone.utc).replace(microsecond=0) + timedelta(hours=3, minutes=30)}")
        await FastAPILimiter.close()

title = getenv('ACC_NAME') if getenv('ACC_NAME') else "Accounting"
app = FastAPI(swagger_ui_parameters={"docExpansion": "none"}, title=title, version="0.1.0.0", lifespan=app_lifespan, debug=True)

WHITELISTED_IPS: List[str] = []
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=["*"], allow_headers=["*"])

route_schema = save_route(routes)
dump(route_schema, open(f'{Path(__file__).parent}/configs/routes.json', 'w'), indent=4)

for route in routes:
    app.include_router(route)
