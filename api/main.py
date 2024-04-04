import os
from typing import List
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from sqlalchemy.exc import OperationalError
import db as dbf
import db.models as models
from db.database import engine, get_db
from lib.log import logger
from router import routes


try:
    # models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(bind=engine)
except OperationalError as e:
    logger.show_log(f"[ Could Not Create Engine ]: {e.__repr__()}", 'e')
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
    Redis_url = os.getenv('LOCAL_REDIS') if os.getenv('LOCAL_POSTGRES') else "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81HBSDsdkjgasdj324@87.107.161.173:6379/0"
    await FastAPILimiter.init(redis=redis.from_url(Redis_url, encoding="utf8"))


@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()


@app.get("/ping", tags=["Ping"])
def ping():
    return "Pong"


@app.get("/count", tags=["Ping"])
async def count(field: str, db=Depends(get_db)):
    status_code, result = dbf.count(db, field)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result


for route in routes:
    app.include_router(route)
