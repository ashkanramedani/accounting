from .business_trip import router as business_trip_route
from .class_cancellation import router as class_cancellation_route
from .employee import router as employee_route
from .leave_request import router as leave_request_route
from .remote_request import router as remote_request_route
from .tardy_request import router as tardy_request_route
from .teacher_replacement import router as teacher_replacement_route

__all__ = [
    "business_trip_route",
    "class_cancellation_route",
    "employee_route",
    "leave_request_route",
    "remote_request_route",
    "tardy_request_route",
    "teacher_replacement_route"]
