import requests
import json
from loguru import logger

class requester():
    def __init__(self):
        self.base_url = "http://127.0.0.1:2030/api/v1/"
        self.headers = {'Content-Type': 'application/json'}        
    
    def get(self, _url):
        data = None

        try: 
            response = requests.request("GET", self.base_url + _url, headers=self.headers)
            data = response.json()
        except Exception as e:
            logger.error('get')
            logger.error(e)

        return data

    def post(self, _url, payload):
        data = None

        try: 
            response = response = requests.request("POST", self.base_url + _url, json=payload, headers=self.headers)
            data = response.json()
        except Exception as e:
            logger.error('post')
            logger.error(e)

        return data