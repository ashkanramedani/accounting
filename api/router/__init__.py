from typing import List, Dict
from fastapi import APIRouter

from .Course import course_route, course_extension_route, sub_course_route, session_route
from .Entity import employee_route, user_route
from .Salary import report_route, salary_policy_route
# from .Site import files, user, post, library
from .Survey_form import question_route, response_route, survey_route
from .User_form import *
from .tools import router as tools_route
from .dropdown import router as dropdown_route
from .Template import router as template_route
from .Status import router as status_route
from .gateway import *
from .Property import router as property_router

ALL: List[APIRouter] = [
    property_router,
    user_route,
    shopping_card_router,
    parsian_route,
    zarinpal_route,
    status_route,
    discount_code_router,
    dropdown_route,
    reward_card_router,
    template_route,
    tools_route,
    employee_route,
    roles_route,
    payment_route,
    course_route,
    sub_course_route,
    session_route,
    course_extension_route,
    report_route,
    salary_policy_route,
    business_trip_route,
    leave_request_route,
    finger_scanner_router,
    remote_request_route,
    request_sub_route,
    tardy_request_route,
    session_cancellation_route,
]

routes_dict: Dict[str, APIRouter] = {str(R.tags): R for R in ALL}
routes: List[APIRouter] = [routes_dict[key] for key in sorted(routes_dict.keys())]

__all__ = ["routes"]
