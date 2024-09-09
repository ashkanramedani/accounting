from .Employee_Forms import business_trip_route, leave_request_route, remote_request_route, finger_scanner_router
from .Teachers_Forms import tardy_request_route, request_sub_route, session_cancellation_route
from .payment import router as payment_route
from .roles import router as roles_route
from .reward_card import router as reward_card_router
from .discount_code import router as discount_code_router

__all__ = [
    "reward_card_router",
    "discount_code_router",
    "session_cancellation_route",
    "business_trip_route",
    "leave_request_route",
    "remote_request_route",
    "finger_scanner_router",
    "tardy_request_route",
    "request_sub_route",
    "payment_route",
    "roles_route"
]
