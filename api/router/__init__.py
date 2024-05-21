from .business_trip import router as business_trip_route
from .course_cancellation import router as course_cancellation_route
from .Course import course_route, course_extension_route, sub_course_route, session_route
from .employee import router as employee_route
from .leave_request import router as leave_request_route
from .payment import router as payment_route
from .question import router as question_route
from .remote_request import router as remote_request_route
from .response import router as response_route
from .student import router as student_route
from .survey import router as survey_route
from .fingerScanner import router as finger_scanner_router
from .Teachers_Forms import teacher_replacement_route, tardy_request_route
from .roles import router as roles_route
from .SalaryPolicy import router as SalaryPolicy_route
from .salary import router as report_route
from .tools import router as tools_route

from .files import router as files
from .user import router as user
from .post import router as post
from .library import router as library

routes = [
    course_route,
    course_extension_route,
    sub_course_route,
    session_route,
    tools_route,
    report_route,
    roles_route,
    business_trip_route,
    course_cancellation_route,
    leave_request_route,
    # question_route,
    remote_request_route,
    # response_route,
    student_route,
    # survey_route,
    # tardy_request_route,
    teacher_replacement_route,
    payment_route,
    finger_scanner_router,
    employee_route,
    SalaryPolicy_route,
    # 
    files,
    user,
    post,
    library
]

__all__ = ["routes"]
