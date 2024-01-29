from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import db.models as models
from db.database import engine
import uvicorn
import redis.asyncio as redis

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from router import employee

models.Base.metadata.create_all(bind=engine)

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
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)

@app.route("/ping")
def ping():
    return "All good. You don't need to be authenticated to call this"
