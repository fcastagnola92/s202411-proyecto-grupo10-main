from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os

from ..config.config import Config

config=Config()

def is_uniqueidentifier(value):
        uuid_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        return bool(uuid_pattern.match(value))

def require_bearer_token(func):
    def wrapper(*args, **kwargs):

    
        if os.environ.get('ENVIRONMENT')=='test':
             return func(*args, **kwargs)
             

        token = request.headers.get("Authorization")



        api_url = f'{config.USERS_PATH}/users/me'

        headers = {
            'Authorization': token
        }  

                

        response = requests.get(api_url, headers=headers)

        response_text = response.text
        status_code = response.status_code


        if status_code==HTTPStatus.OK:
            return func(*args, **kwargs)
        else:
            return (response_text, status_code) 
            

    return wrapper