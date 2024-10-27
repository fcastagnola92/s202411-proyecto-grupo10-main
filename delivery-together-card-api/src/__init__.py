from flask import Flask
from .config.config import Config

config = Config()



def create_app(config_name):
    app = Flask(__name__)
    app.config['USERS_PATH'] = config.USERS_PATH
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
    if config.DB_USER is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/route-db'

    return app

from .app import *