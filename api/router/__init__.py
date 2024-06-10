from .Employee_Forms import business_trip_route, leave_request_route, remote_request_route, finger_scanner_router
from .Course import course_route, course_extension_route, sub_course_route, session_route
from .Teachers_Forms import tardy_request_route, request_sub_route
from .Survey_form import question_route, response_route, survey_route
from .Salary import report_route, SalaryPolicy_route

from .employee import router as employee_route
from .payment import router as payment_route
from .student import router as student_route
from .roles import router as roles_route
from .tools import router as tools_route

from .files import router as files
from .user import router as user
from .post import router as post
from .library import router as library


routes = [
    request_sub_route,
    course_route,
    course_extension_route,
    sub_course_route,
    session_route,
    tools_route,
    report_route,
    roles_route,
    business_trip_route,
    leave_request_route,
    # question_route,
    remote_request_route,
    # response_route,
    student_route,
    # survey_route,
    tardy_request_route,
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
