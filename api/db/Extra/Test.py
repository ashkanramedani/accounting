from contextlib import contextmanager

from fastapi import APIRouter
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

from db.Extra import Return_Test_Exception
from lib import logger
from schemas import Route_Result

@contextmanager
def create_client(router: APIRouter) -> TestClient:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()

def Test_CRUD(router: APIRouter):
    Result_Obj = []

    with create_client(router) as client:
        end_point = f"/{router.prefix}/search"
        try:
            response = client.get(end_point)
            Result_Obj.append(Route_Result(route=end_point, status=response.status_code, body=str(response.json())))
        except Exception as E:
            logger.error(E)
            # return Return_Test_Exception(E)

        return 200, Result_Obj
