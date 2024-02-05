from .teacher_replacement import *
from .class_cancellation import *
from .remote_request import *
from .business_trip import *
from .leave_request import *
from .tardy_request import *
from .employee import *
from .student import *


__all__ = [
    "get_employee",
    "get_all_employee",
    "post_employee",
    "delete_employee",
    "update_employee",
    "get_student",
    "post_student",
    "delete_student",
    "update_student",
    "get_leave_request",
    "get_all_leave_request",
    "post_leave_request",
    "delete_leave_request",
    "update_leave_request",
    "get_tardy_request",
    "get_all_tardy_request",
    "post_tardy_request",
    "delete_tardy_request",
    "update_tardy_request",
    "get_teacher_replacement",
    "get_all_teacher_replacement",
    "post_teacher_replacement",
    "delete_teacher_replacement",
    "update_teacher_replacement",
    "get_business_trip_form",
    "get_all_business_trip_form",
    "post_business_trip_form",
    "delete_business_trip_form",
    "update_business_trip_form",
    "get_class_cancellation_form",
    "get_all_class_cancellation_form",
    "post_class_cancellation_form",
    "delete_class_cancellation_form",
    "update_class_cancellation_form",
    "get_remote_request_form",
    "get_all_remote_request_form",
    "post_remote_request_form",
    "delete_remote_request_form",
    "update_remote_request_form"
]
