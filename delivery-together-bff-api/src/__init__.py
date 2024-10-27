from flask import Flask
from .config.config import Config

config = Config()



def create_app(config_name):
    app = Flask(__name__)
    app.config['USERS_PATH'] = config.USERS_PATH

    return app

from .app import *