from .Course import course_route, course_extension_route, sub_course_route, session_route
from .Employee_Forms import business_trip_route, leave_request_route, remote_request_route, finger_scanner_router
from .Salary import report_route, SalaryPolicy_route
from .Survey_form import question_route, response_route, survey_route
from .Teachers_Forms import tardy_request_route, request_sub_route
from .employee import router as employee_route
from .files import router as files
from .library import router as library
from .payment import router as payment_route
from .post import router as post
from .roles import router as roles_route
from .student import router as student_route
from .tools import router as tools_route
from .user import router as user

routes = [
    # Test Env
    tools_route,

    # Entity
    student_route,
    employee_route,


    # User Form
    roles_route,
    payment_route,

    # Course
    course_route,
    sub_course_route,
    session_route,
    course_extension_route,

    # Salary
    report_route,
    SalaryPolicy_route,

    # Employee Form
    business_trip_route,
    leave_request_route,
    finger_scanner_router,
    remote_request_route,

    # Teacher Form
    request_sub_route,
    tardy_request_route,


    # Survey
    # question_route,
    # response_route,
    # survey_route,

    # Site Form
    files,
    user,
    post,
    library
]

__all__ = ["routes"]
