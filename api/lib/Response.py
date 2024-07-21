from typing import Any

from fastapi import HTTPException

Success_Code = [200, 201]


def create_Response(status_code: int, detail: Any):
    if status_code in Success_Code:
        return detail
    raise HTTPException(status_code=status_code, detail=detail)
