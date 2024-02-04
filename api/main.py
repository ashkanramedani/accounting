from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import db.models as models
from db.database import engine
import uvicorn
import redis.asyncio as redis
from sqlalchemy.exc import OperationalError
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from lib import log
from router import employee
from router import form

Logger = log()

try:
    models.Base.metadata.create_all(bind=engine)
except OperationalError as e:
    Logger.show_log(f"[ Could Not Create Engine ]: {e}", 'e')


app = FastAPI()
WHITELISTED_IPS = []


@app.on_event("startup")
async def startup():
    r = redis.from_url("redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0", encoding="utf8")
    await FastAPILimiter.init(r)


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()


app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(employee.router)
app.include_router(form.router)


@app.get("/ping")
def ping():
    return "All good. You don't need to be authenticated to call this"
