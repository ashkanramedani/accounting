from .business_trip import *
from .class_cancellation import *
from .classes import *
from .employee import *
from .leave_request import *
from .remote_request import *
from .student import *
from .Survey import *
from .response import *
from .tardy_request import *
from .teacher_replacement import *
from .payment import *

__all__ = [
    # employee.py
    "get_employee",
    "get_all_employee",
    "post_employee",
    "delete_employee",
    "update_employee",
    # student.py
    "get_student",
    "get_all_student",
    "post_student",
    "delete_student",
    "update_student",
    # leave_request.py
    "get_leave_request",
    "get_all_leave_request",
    "post_leave_request",
    "delete_leave_request",
    "update_leave_request",
    # tardy_request.py
    "get_tardy_request",
    "get_all_tardy_request",
    "post_tardy_request",
    "delete_tardy_request",
    "update_tardy_request",
    # teacher_replacement.py
    "get_teacher_replacement",
    "get_all_teacher_replacement",
    "post_teacher_replacement",
    "delete_teacher_replacement",
    "update_teacher_replacement",
    # business_trip.py
    "get_business_trip_form",
    "get_all_business_trip_form",
    "post_business_trip_form",
    "delete_business_trip_form",
    "update_business_trip_form",
    # class_cancellation.py
    "get_class_cancellation_form",
    "get_all_class_cancellation_form",
    "post_class_cancellation_form",
    "delete_class_cancellation_form",
    "update_class_cancellation_form",
    # remote_request.py
    "get_remote_request_form",
    "get_all_remote_request_form",
    "post_remote_request_form",
    "delete_remote_request_form",
    "update_remote_request_form",
    # survey.py
    # 1.question
    "get_question",
    "get_all_question",
    "post_question",
    "delete_question",
    "update_question",
    # 2.survey
    "get_survey",
    "get_all_survey",
    "post_survey",
    "delete_survey",
    "update_survey",
    # "update_survey_question",
    # response.py
    "get_response",
    "get_all_response",
    "post_response",
    "delete_response",
    "update_response",
    # class.py
    "get_class",
    "get_all_class",
    "post_class",
    "delete_class",
    "update_class",
    # payment.py
    "get_payment_method",
    "get_all_payment_method",
    "post_payment_method",
    "delete_payment_method",
    "update_payment_method"
]
