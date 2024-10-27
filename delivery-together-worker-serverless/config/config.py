import os

class Config:
    TRUENATIVE_BASE_URL = os.environ.get('TRUENATIVE_BASE_URL')
    TRUENATIVE_SECRET_TOKEN = os.environ.get('TRUENATIVE_SECRET_TOKEN')
    CARD_BASE_URL = os.environ.get('CARD_BASE_URL')