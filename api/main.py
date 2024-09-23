try:
    from os import getenv
    from typing import List
    from pathlib import Path
    from json import dump, load
    from time import sleep, time
    from dotenv import load_dotenv
    from datetime import datetime, timedelta, timezone

    # DB
    from redis import asyncio as redis

    # fastApi
    from fastapi import FastAPI, Request
    from fastapi_limiter import FastAPILimiter
    from contextlib import asynccontextmanager
    from fastapi.middleware.cors import CORSMiddleware

except (ImportError, ModuleNotFoundError):
    raise Exception('Requirement Not Satisfied: some_module is missing')

from router import routes
from lib import logger
from db import save_route
from models import SetUp, Create_engine, Create_Redis_URL, sessionmaker, SetUp_table

print(f'{" -.-" * 10}\n\t\tStarting API\n{" -.-" * 10}')

config = load(open("configs/config.json"))
IRAN_TIMEZONE = timezone(offset=timedelta(hours=3, minutes=30))


@asynccontextmanager
async def app_lifespan(api):
    try:
        logger.info(f"preparing {api.title} V: {api.version} - {datetime.now(tz=IRAN_TIMEZONE)}")
        engine = Create_engine(config.get("db", None))
        res = SetUp_table(engine)
        if not res:
            logger.error("Database Setup failed")
            raise Exception

        if not getenv('MODE') == "DEBUG":
            with sessionmaker(autoflush=False, bind=engine)() as Tmp_Connection:
                SetUp(Tmp_Connection)

        redis_obj = redis.from_url(Create_Redis_URL(config.get("redis", None)), encoding="utf8")
        await FastAPILimiter.init(redis=redis_obj)

        logger.info(f'{api.title} V: {api.version} Has been started ...')
        yield
    finally:
        logger.info(f'Exiting from {api.title} V: {api.version} - {datetime.now(tz=IRAN_TIMEZONE)}')
        await FastAPILimiter.close()


load_dotenv()
app = FastAPI(
        lifespan=app_lifespan,
        version=config["versions"],
        swagger_ui_parameters={"docExpansion": "none"},
        title=getenv('ACC_NAME') if getenv('ACC_NAME') else config["title"],
        debug=getenv('SWAGGER_DEBUG') if getenv('SWAGGER_DEBUG') else config["debug"])

WHITELISTED_IPS: List[str] = []

# Set up CORS middleware
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
)

METHOD = {
    "GET": "GET",
    "POST": "PST",
    "PUT": "PUT",
    "DELETE": "DEL",
    "PATCH": "PAT",
    "OPTIONS": "OPT"
}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # start_time = time()

    response = await call_next(request)
    # try:
    #     logger.log("INFO_access", f"[ {time() - start_time:.3f}s ] {response.status_code} / {METHOD[request.method]: >3} - {request.url}")
    # except ValueError:
    #     pass

    # response.headers["X-Process-Time"] = f'{time() - start_time:.5f}'
    return response

if getenv('CREATE_ROUTE_SCHEMA'):
    logger.info('Creating Route Schema')
    route_schema = save_route(routes)
    dump(route_schema, open(f'{Path(__file__).parent}/configs/routes.json', 'w'), indent=4, sort_keys=True)

logger.info(f"Loading Routes to API")
for route in routes:
    app.include_router(route)
