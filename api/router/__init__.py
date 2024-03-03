from .business_trip import router as business_trip_route
from .class_cancellation import router as class_cancellation_route
from .classes import router as class_route
from .employee import router as employee_route
from .leave_request import router as leave_request_route
from .payment import router as route_payment
# from .question import router as question_route
from .remote_request import router as remote_request_route
# from .response import router as response_route
# from .student import router as student_route
# from .survey import router as survey_route
from .tardy_request import router as tardy_request_route
from .teacher_replacement import router as teacher_replacement_route
# from .fingerScanner import router as finger_scanner_router

from .files import router as files
from .user import router as user
from .post import router as post
from .tag import router as tag
from .category import router as category
from .library import router as library

routes = [
    business_trip_route,
    class_cancellation_route,
    class_route,
    employee_route,
    leave_request_route,
    # question_route,
    remote_request_route,
    # response_route,
    # student_route,
    # survey_route,
    tardy_request_route,
    teacher_replacement_route,
    route_payment,
    # fingerscanner_router,

    files,
    user,
    post,
    tag,
    category,
    library
]

__all__ = ["routes"]
