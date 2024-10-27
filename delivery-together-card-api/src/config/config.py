import os

class Config:
    APP_NAME = os.environ.get('APP_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT') 
    DB_NAME = os.environ.get('DB_NAME')
    USERS_PATH = os.environ.get('USERS_PATH')
    NATIVE_PATH=os.environ.get('NATIVE_PATH')
    NATIVE_TOKEN=os.environ.get('NATIVE_TOKEN')
    PROJECT_ID=os.environ.get('PROJECT_ID')
    TOPIC=os.environ.get('TOPIC')