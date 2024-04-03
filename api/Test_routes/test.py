import os
from datetime import datetime, date, time, timedelta
from time import sleep
import random
import requests
from loguru import logger
from typing import List
from random import choice as rnd
from faker import Faker


class Person:
    def __init__(self):
        self.unique_names = []
        self.fake = Faker()

    def iterate(self):
        return f'{self.fake.first_name()}-{self.fake.last_name()}'

    def generate_name(self, unique: bool = True):
        if not unique and self.unique_names:
            return rnd(self.unique_names).split('-')
        tmp = self.iterate()
        while tmp in self.unique_names:
            tmp = self.iterate()
        self.unique_names.append(tmp)
        return tmp.split('-')


person = Person()
faker_Q = Faker()
Base = "http://localhost:5001"
# Base = "https://admin.api.ieltsdaily.ir"
DATE_STRING = str(datetime.now())
Routes: List[str] = ['api/v1/form/fingerprint_scanner']
ROLE = ["teacher", "office", "rd", "supervisor"]


def send_request(method, url, data: dict | str = '', return_data=False) -> dict | None:
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.request(url=url, method=method, headers=headers, json=data)
    except TypeError:
        headers = {'accept': 'application/json'}
        response = requests.request(url=url, method=method, headers=headers, files=data)
    sleep(.5)

    if response.status_code == 200:
        logger.opt(depth=1).info(f'{url} ,200,{response.text}')
        if not response.json():
            logger.warning(f"Could Not Get Data From Server: url")
            exit()
        if return_data:
            return response.json()
    else:
        if "IntegrityError('(psycopg2.errors.UniqueViolation)" in response.text:
            logger.opt(depth=1).warning(f'{url} ,UniqueViolation')
        else:
            logger.opt(depth=1).error(f'{url} ,{response.status_code},{response.text}')


def All_Employees(include_admin: bool = False):
    Res = requests.request(method="get", url=f"{Base}/api/v1/employee/search").json()
    if not Res:
        print("No EMPLOYEE FOUND")
        exit()
    if include_admin:
        return [emp for emp in Res]
    return [emp for emp in Res if emp["name"] != "Admin"]


def employee_data(all_ROLE, FID: int):
    while True:
        name, last_name = person.generate_name()
        yield {'name': name, 'last_name': last_name, 'day_of_birth': str(datetime.now()), 'email': '', 'mobile_number': '', 'id_card_number': '', 'address': '', 'priority': 5, 'fingerprint_scanner_user_id': FID, "roles": [rnd(all_ROLE)["role_pk_id"]]}


def student_data():
    while True:
        name, last_name = person.generate_name()
        yield {'name': name, 'last_name': last_name, 'day_of_birth': str(datetime.now()), 'email': '', 'mobile_number': '', 'id_card_number': '', 'address': '', 'level': ''}


def class_data(created, all_EMP):
    while True:
        yield {"created_fk_by": created, "teachers": [rnd(all_EMP)["employees_pk_id"]], "name": "NOT SPECIFIED", "class_time": str(datetime.now()), "duration": 60}


def leave_data(created, all_EMP):
    while True:
        yield {"created_fk_by": created, "description": "description", "employee_fk_id": rnd(all_EMP)["employees_pk_id"], "end_date": DATE_STRING, "start_date": DATE_STRING, "status": 0}


def question_data(created):
    while True:
        yield {"created_fk_by": created, "text": faker_Q.sentence(), "language": random.choice(["en", "fa", "fr", "de", "es"])}


def remote_data(created, all_EMP):
    while True:
        yield {"created_fk_by": created, "description": "description", "employee_fk_id": rnd(all_EMP)["employees_pk_id"], "end_date": DATE_STRING, "start_date": DATE_STRING, "status": 0, "working_location": "working_location"}


def business_data(created, all_EMP):
    while True:
        yield {"created_fk_by": created, "description": "description", "destination": "destination", "employee_fk_id": rnd(all_EMP)["employees_pk_id"], "end_date": DATE_STRING, "start_date": DATE_STRING, "status": 0}


def payment_data(created, all_EMP):
    while True:
        yield {"card_number": "000000000000000", "created_fk_by": created, "description": "description", "employee_fk_id": rnd(all_EMP)["employees_pk_id"], "shaba": "0000000000000000", "status": 0}


def fingerprint_data(created, file: bool = True):
    if file:
        for file_path in [os.path.abspath(os.path.join("data", file)) for file in os.listdir("./data") if file.endswith("csv")]:
            yield {'file': ('t.csv', open(file_path, 'rb'), 'text/csv')}

    else:
        name, _ = person.generate_name()
        Date = datetime.now()
        Enter = str(Date.time())
        Exit = str((Date + timedelta(hours=1)).time())
        yield {"created_fk_by": created, "EnNo": random.randint(1000000, 9999999), "Name": name, "Date": str(Date.date()), "Enter": Enter, "Exit": Exit}

def role_data(created):
    for i in ["teacher", "office", "rd", "supervisor", "admin"]:
        yield {'name': i, 'cluster': "cluster", "created_fk_by": created}

def Salary_data(created, all_EMP):
    if random.random() > 0.5:
        yield {"created_fk_by": created, 'employee_fk_id': rnd(all_EMP)["employees_pk_id"], "day_starting_time": "09:00:00", "day_ending_time": "16:30:00", "Regular_hours_factor": 1, "overtime_permission": 1, "overtime_factor": 1, "overtime_cap": 3600, "overtime_threshold": 1, "undertime_factor": 1, "undertime_threshold": 15, "off_day_permission": 1, "off_day_factor": 1, "off_day_cap": 400, "remote_permission": 1, "remote_factor": 1, "remote_cap": 3600, "medical_leave_factor": 0, "medical_leave_cap": 2, "vacation_leave_factor": 1, "vacation_leave_cap": 2, "business_trip_permission": 1, "business_trip_factor": 1, "business_trip_cap": 1800}
    else:
        yield {"created_fk_by": created, 'employee_fk_id': rnd(all_EMP)["employees_pk_id"], "Regular_hours_factor": 1, "Regular_hours_cap": 450, "overtime_permission": 1, "overtime_factor": 1, "overtime_cap": 3600, "overtime_threshold": 1, "undertime_factor": 1, "undertime_threshold": 15, "off_day_permission": 1, "off_day_factor": 1, "off_day_cap": 400, "remote_permission": 1, "remote_factor": 1, "remote_cap": 3600, "medical_leave_factor": 0, "medical_leave_cap": 2, "vacation_leave_factor": 1, "vacation_leave_cap": 2, "business_trip_permission": 1, "business_trip_factor": 1, "business_trip_cap": 1800}

def entity(emp: int, cls: int, std: int, Q: int):
    # Admin
    data = {'name': "Admin", 'last_name': "Admin", 'day_of_birth': str(datetime.now()), 'email': '', 'mobile_number': '', 'id_card_number': '', 'address': '', 'priority': 5, 'fingerprint_scanner_user_id': 3}
    send_request(method="post", url=f"{Base}/api/v1/employee/add", data=data)

    created = [emp for emp in All_Employees(include_admin=True) if emp["name"] == "Admin"][0]["employees_pk_id"]
    # Role
    for data in role_data(created):

        send_request(method="post", url=f"{Base}/api/v1/form/role/add", data=data)

    all_ROLE = send_request(method="get", url=f"{Base}/api/v1/form/role/search", return_data=True)

    F_ID = [4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17]
    # Employee
    for i in range(emp):
        if i < len(F_ID):
            send_request(method="post", url=f"{Base}/api/v1/employee/add", data=next(employee_data(all_ROLE, F_ID[i])))
        else:
            send_request(method="post", url=f"{Base}/api/v1/employee/add", data=next(employee_data(all_ROLE, F_ID[i] % len(F_ID))))

    all_EMP = All_Employees()

    # Student
    for i in range(std):
        send_request(method="post", url=f"{Base}/api/v1/form/student/add", data=next(student_data()))

    # Class
    for i in range(cls):
        send_request(method="post", url=f"{Base}/api/v1/form/class/add", data=next(class_data(created, all_EMP)))

    # Question
    for i in range(Q):
        send_request(method="post", url=f"{Base}/api/v1/form/question/add", data=next(question_data(created)))


def employee_related_forms(TOTAL: int):
    all_EMP = All_Employees()
    created = [emp for emp in All_Employees(include_admin=True) if emp["name"] == "Admin"][0]["employees_pk_id"]

    for _ in range(TOTAL):
        send_request(method="post", url=f"{Base}/api/v1/form/leave_request/add", data=next(leave_data(created, all_EMP)))
        send_request(method="post", url=f"{Base}/api/v1/form/remote_request/add", data=next(remote_data(created, all_EMP)))
        send_request(method="post", url=f"{Base}/api/v1/form/business_trip/add", data=next(business_data(created, all_EMP)))
        send_request(method="post", url=f"{Base}/api/v1/form/payment_method/add", data=next(payment_data(created, all_EMP)))

    for i in fingerprint_data(created):
        send_request(method="post", url=f"{Base}/api/v1/form/fingerprint_scanner/bulk_add/{created}", data=i)

    for i in range(10):
        send_request(method="post", url=f"{Base}/api/v1/form/fingerprint_scanner/add", data=next(fingerprint_data(created, file=False)))
def teacher_related(TOTAL: int):
    pass

if __name__ == '__main__':
    entity(emp=3, cls=1, std=1, Q=1)
    employee_related_forms(TOTAL=1)
    teacher_related(TOTAL=5)
