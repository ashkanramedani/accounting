from typing import List

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy.exc import OperationalError

import db.models as models
from db.database import engine
from lib import log
from router import routes

Logger = log()

try:
    models.Base.metadata.create_all(bind=engine)
except OperationalError as e:
    Logger.show_log(f"[ Could Not Create Engine ]: {e.__repr__()}", 'e')
    exit()

app = FastAPI()
WHITELISTED_IPS: List[str] = []
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = redis.from_url("redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0", encoding="utf8")
    await FastAPILimiter.init(r)


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()


@app.get("/ping", tags=["Ping"])
def ping():
    return "Pong"


for route in routes:
    app.include_router(route)


