print(f'\n{" -.-" * 11}\n\t\tStarting API\n{" -.-" * 11}')

try:
    from os import getenv
    from re import search
    from typing import List
    from pathlib import Path
    from json import dump, load, loads
    from time import sleep, time
    from dotenv import load_dotenv
    from datetime import datetime, timedelta, timezone

    # DB
    from redis import asyncio as redis
    from sqlalchemy.orm import sessionmaker

    # fastApi
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi_limiter import FastAPILimiter
    from contextlib import asynccontextmanager
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.responses import Response

except (ImportError, ModuleNotFoundError):
    raise Exception('Requirement Not Satisfied: some_module is missing')

try:
    from db import save_route
    from lib import logger, access_log
    from models import SetUp, Create_Redis_URL, SetUp_table
    from router import routes
    from typing import Dict
    from models.Dependency import engine

except ImportError as e:
    raise ImportError(f'{e.__class__.__name__}: {e.__repr__()}')

load_dotenv()

config: Dict = load(open("configs/config.json"))
IRAN_TIMEZONE: timezone = timezone(offset=timedelta(hours=3, minutes=30))


@asynccontextmanager
async def app_lifespan(api):
    logger.info(f"preparing {api.title} V: {api.version}")
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

    logger.info(f'Exiting from {api.title} V: {api.version}')
    await FastAPILimiter.close()


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


BlackList = ["/openapi.json", '/docs', '/']

@app.middleware("http")
async def Access(request: Request, call_next):
    start_time = time()
    try:
        request_body = await request.body()
        request_body = request_body.decode('utf-8')

        try:
            request_body = loads(request_body)
        except Exception as E:
            pass

        response = await call_next(request)
        body = b"".join([chunk async for chunk in response.body_iterator])
        if str(search(r"https?://[^:/]+:\d+(/[^?]*)", str(request.url)).group(1)) in BlackList:
            response_body = None
        else:
            response_body = body.decode()
        response = Response(content=body, status_code=response.status_code, headers=dict(response.headers))

    except Exception as Access_error:
        request_body = None
        response_body = f"Error in parsing: {Access_error.__class__.__name__} - {Access_error.args}"
        response = Response(content=f"Error processing request: {response_body}", status_code=500)

    end_time = time()

    Additional_data = {"request_body": request_body, "response_body": response_body}
    access_log.info(f"[ {end_time - start_time:.3f}s ] - {request.method} - {request.url}", **Additional_data)
    return response


if getenv('CREATE_ROUTE_SCHEMA'):
    logger.info('Creating Route Schema')
    route_schema = save_route(routes)
    dump(route_schema, open(f'{Path(__file__).parent}/configs/routes.json', 'w'), indent=4, sort_keys=True)

logger.info(f"Loading Routes to API")
for route in routes:
    app.include_router(route)
