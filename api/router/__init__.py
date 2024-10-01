from .Course import course_route, course_extension_route, sub_course_route, session_route
from .Entity import student_route, employee_route
from .Salary import report_route, salary_policy_route
from .Site import files, user, post, library
from .Survey_form import question_route, response_route, survey_route
from .User_form import *
from .tools import router as tools_route
from .dropdown import router as dropdown_route
from .Template import router as template_route
from .Status import router as status_route

# routes = [
#     report_route,
#     finger_scanner_router,
#     salary_policy_route,
#     employee_route,
#     tools_route
# ]

routes = [
    status_route,
    discount_code_router,
    # dropdown_route
    dropdown_route,

    reward_card_router,
    # Template
    template_route,

    # Router_test Env
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
    salary_policy_route,

    # Employee Form
    business_trip_route,
    leave_request_route,
    finger_scanner_router,
    remote_request_route,

    # Teacher Form
    request_sub_route,
    tardy_request_route,
    session_cancellation_route,

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
