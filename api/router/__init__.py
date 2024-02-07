from .business_trip import router as business_trip_route
from .class_cancellation import router as class_cancellation_route
from .classes import router as class_route
from .employee import router as employee_route
from .leave_request import router as leave_request_route
from .question import router as question_route
from .remote_request import router as remote_request_route
from .response import router as response_route
from .student import router as student_route
from .survey import router as survey_route
from .tardy_request import router as tardy_request_route
from .teacher_replacement import router as teacher_replacement_route
from .payment import router as route_payment

routes = [
    business_trip_route,
    class_cancellation_route,
    class_route,
    employee_route,
    leave_request_route,
    question_route,
    remote_request_route,
    response_route,
    student_route,
    survey_route,
    tardy_request_route,
    teacher_replacement_route,
    route_payment]


'''
{
  "detail": "IntegrityError('(psycopg2.errors.ForeignKeyViolation) insert or update on table
   \"payment_method\" violates foreign key constraint \"payment_method_employee_fk_id_fkey\"
   \\nDETAIL:  Key (employee_fk_id)=(3fa85f64-5717-4562-b3fc-2c963f66afa6) is not present in table \"employees\".\\n')"
}
'''