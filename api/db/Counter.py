import db.models as dbm

Tables = {
    "survey": dbm.Survey_form,
    "Post": dbm.Posts,
    "role": dbm.Roles_form,
    "Remote Request": dbm.Remote_Request_form,
    "question": dbm.Questions_form,
    "response": dbm.Response_form,
    "Business Trip": dbm.Business_Trip_form,
    "Class Cancellation": dbm.Class_Cancellation_form,
    "Employee": dbm.Employees_form,
    "Tardy Request": dbm.Teacher_tardy_reports_form,
    "Student": dbm.Student_form,
    "Teacher Replacement": dbm.Teacher_Replacement_form,
    "class": dbm.Class_form,
    "fingerprint_scanner": dbm.Fingerprint_scanner_form,
    "payment_method": dbm.Payment_method_form,
    "Leave Forms":dbm.Leave_request_form
}

def count(db, table: str):
    if table not in Tables:
        return 404, "Table Not Found"

    return 200, len(db.query(Tables[table]).filter_by(deleted=False).all())