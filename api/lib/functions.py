import sys
import os
import hashlib
import time
import requests
import re
import random
from typing import Dict, Any
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil import parser
from datetime import date, timedelta, datetime
from persiantools.jdatetime import JalaliDate
from khayyam import JalaliDatetime

from lib.json_handler import json_handler
from lib.redis_db import Redis
from lib.log import log
from lib.hash import Hash   
import logging

_objLog = log()
directory = os.getcwd()
_obj_json_handler_config = json_handler(FilePath=directory +"/configs/config.json")

config =  _obj_json_handler_config.Data

successCode = [200,201]

def get(url, headers={'Content-Type': 'application/json'}):
    return requests.request("GET", url, headers=headers)

def put(url, body, headers={'Content-Type': 'application/json'}):
    return requests.request("PUT", url, json=body, headers=headers)

def post(url, body, headers={'Content-Type': 'application/json'}):
    return requests.request("POST", url, json=body, headers=headers)


class Tools:
    def __init__(self) -> None:
        pass

    def generate_reset_password_link(self, user_id: int, username: str) -> str:
        _datetime = str(datetime.now())
        _obj_redis = Redis(config=config['redis_reset_password'])
        _hash_value = Hash.hash_generator(username+_datetime)

        if _obj_redis.set_key(_hash_value, user_id, 24*60*60):
            link = f"{config['resetpassword']['url']}{_hash_value}"
            return link, _hash_value
        else: 
            return False, None

    def generate_verify_link(self, user_id: int, username: str):
        _datetime = str(datetime.now())
        _obj_redis = Redis(config=config['redis_verify_link'])
        _hash_value = Hash.hash_generator(username+_datetime)

        if _obj_redis.set_key(_hash_value, user_id, 24*60*60):
            link = f"{config['verify']['url']}{hash_value}"
            return link, _hash_value
        else: 
            return False, None

    def check_code_otp(self, code):
        res = {
            "mobile_number": None,
            "is_existed": False
        }

        _obj_redis = Redis(config=config['redis_otp'])

        if _obj_redis.key_exists(code):
            res["is_existed"] = True
            res["mobile_number"] = _obj_redis.get_key(code)

        return res
    
    def generate_code_otp(self, mobile_number):
        _code = random.randint(10000,99999)
        _obj_redis = Redis(config=config['redis_otp'])

        if _obj_redis.set_key( _code, mobile_number, 10*60):        
            return _code
        else: 
            return False

class ToolsForTimToBook:
    def __init__(self) -> None:
        pass

    def get_holyday_time(self, month=None):
        url = "https://www.taghvim.com/get_events"
        payload = ""
        headers = {"x-requested-with": "XMLHttpRequest"}        
        res = {}
        if month is None:
            for _month in range(1,13):
                querystring = {"action":"get_events","month":str(_month),"_":str(int(time.time()))}
                response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
                if response.status_code in successCode:
                    res[str(_month)] = response.json()
                else:
                    res[str(_month)] = []
        else:
            querystring = {"action":"get_events","month":str(_month),"_":str(int(time.time()))}
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code in successCode:
                res[str(_month)] = response.json()
            else:
                res[str(_month)] = []
        
        return res

    def generate_exam_schedule(self, start_date, end_date, selected_days, start_time, end_time, time_slot_minutes, schedule_exceptions) -> Any:
        exam_schedule = []

        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in selected_days:
                current_time = JalaliDatetime.combine(current_date, start_time)
                end_of_day = JalaliDatetime.combine(current_date, end_time)
                while current_time < end_of_day:
                    if str(current_time)[:10] not in schedule_exceptions:

                        x = {
                            "day_of_week": current_date.weekday(),
                            "start_date": str(current_time)[:10],
                            "end_date": str(current_time)[:10],
                            "start_time": (current_time)._time,
                            "end_time": (current_time + timedelta(minutes=time_slot_minutes))._time,
                        }
                        exam_schedule.append(x)
                    current_time += timedelta(minutes=time_slot_minutes)

            current_date += timedelta(days=1)

        return exam_schedule
class Massenger:
    def __init__(self) -> None:
        pass
    
    def send_sms_fast(self, mobile_numbers, template_id, parameter_array):
        data = { 
            "parameter_array": parameter_array,
            "template_id": template_id,
            "mobile_numbers": mobile_numbers
        }

        try:
            response = post(config["fast_sms"]["url"], body=data)  
            _objLog.show_log(config["fast_sms"]["url"] ,'e') 
            _objLog.show_log(data ,'e') 
            _objLog.show_log(response.json ,'e') 
            _objLog.show_log(response.status_code ,'e') 
            if response.status_code in successCode:
                return response.status_code, response.json(), None
            else:
                return response.status_code, [], 'Error'
        except Exception as e:
            _objLog.show_log(e ,'e')
        return False

    def send_email(self, subject, messages, to):
        data = {
            "to": to,
            "subject": subject,
            "message": messages
        }

        try:
            response = post(config["email"]["url"], body=data)
            if response.status_code in successCode:
                return response.status_code, response.json(), None
            else:
                return response.status_code, [], 'Error'
        except Exception as e:
            _objLog.show_log(e,'e')
        return False