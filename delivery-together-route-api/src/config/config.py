import os

class Config:
    APP_NAME = os.environ.get('APP_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT') 
    DB_NAME = os.environ.get('DB_NAME')
    USERS_PATH = os.environ.get('USERS_PATH')