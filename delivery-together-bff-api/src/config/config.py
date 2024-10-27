import os

class Config:
    APP_NAME = os.environ.get('APP_NAME')
    USERS_PATH = os.environ.get('USERS_PATH')
    OFFER_PATH = os.environ.get('OFFER_PATH')
    SCORE_PATH = os.environ.get('SCORE_PATH')
    ROUTE_PATH = os.environ.get('ROUTE_PATH')
    POST_PATH = os.environ.get('POST_PATH')