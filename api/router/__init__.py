from .business_trip import router as business_trip_route
from .course_cancellation import router as course_cancellation_route
from .course import router as course_route
from .employee import router as employee_route
from .leave_request import router as leave_request_route
from .payment import router as route_payment
from .question import router as question_route
from .remote_request import router as remote_request_route
from .response import router as response_route
from .student import router as student_route
from .survey import router as survey_route
from .fingerScanner import router as finger_scanner_router
from .tardy_request import router as tardy_request_route
from .teacher_replacement import router as teacher_replacement_route
from .roles import router as roles_route
from .SalaryPolicy import router as salary_route
from .salary import router as report_route
from .tools import router as tools_route

from .files import router as files
from .user import router as user
from .post import router as post
from .tag_category import router as tag_category_route
from .library import router as library

routes = [
    tag_category_route,
    tools_route,
    report_route,
    roles_route,
    business_trip_route,
    course_cancellation_route,
    course_route,
    leave_request_route,
    salary_route,
    question_route,
    remote_request_route,
    response_route,
    student_route,
    survey_route,
    tardy_request_route,
    teacher_replacement_route,
    route_payment,
    finger_scanner_router,
    employee_route,

    files,
    user,
    post,
    library
]

__all__ = ["routes"]
