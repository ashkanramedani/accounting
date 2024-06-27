from typing import Any, List

from fastapi.testclient import TestClient
from router.Course import course_route
from pydantic import BaseModel
from lib import logger

class Route_Result(BaseModel):
    route: str
    status: int
    body: Any


class Result(BaseModel):
    result: List[Route_Result] = []


def Course_Get_All(Course_client: TestClient):
    res = Course_client.get("/search")
    return Route_Result(route="/search", status=res.status_code, body=res.json)

def Course():
    logger.info("[DEV] Course Started")
    Result_Obj = Result()
    Course_client = TestClient(course_route)
    Result_Obj.result.append(Course_Get_All(Course_client))
    return Result


"""
    Result_Obj.result.append(Course_Get_All(Course_client))
AttributeError: type object 'Result' has no attribute 'result'
"""