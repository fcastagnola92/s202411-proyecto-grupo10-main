
from flask_restful import Resource, Api
from flask import Flask, request, json

from src import create_app
from .config.config import Config
from .dataContext.sqlAlchemyContext import db
from .views import PingView,ResetCardsView,CardView,UpdateCardView, CardListView,CardPendingView
import re
import signal
import logging



config = Config()


app = create_app('default')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('default')

logger.info('Starting application')


def before_server_stop(*args, **kwargs):
    logger.info('Closing database connections ...')
    db.session.remove()

signal.signal(signal.SIGTERM, before_server_stop)




app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
#resources
api.add_resource(PingView, '/credit-cards/ping', endpoint='credit-cards_ping')
api.add_resource(ResetCardsView, '/credit-cards/reset', endpoint='cards_reset')
api.add_resource(CardView,'/credit-cards',endpoint='cards')
api.add_resource(CardListView,'/credit-cards',endpoint='credit-cards')
api.add_resource(UpdateCardView,'/credit-cards/resolve/<string:id_card>',endpoint='resolve_verification')
api.add_resource(CardPendingView,'/credit-cards/pending',endpoint='pending')


