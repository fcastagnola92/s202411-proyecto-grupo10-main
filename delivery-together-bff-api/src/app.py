
from flask_restful import Resource, Api
from flask import Flask, request, json

from src import create_app
from .config.config import Config
from .views import PingView
from .views.offers.OfferView import OfferView
from .views.posts.PostsView import PostsView
import re
import signal
import logging



config = Config()


app = create_app('default')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('default')

logger.info('Starting application')


def before_server_stop(*args, **kwargs):
    logger.info('Closing application ...')


signal.signal(signal.SIGTERM, before_server_stop)




app_context = app.app_context()
app_context.push()


api = Api(app)
#resources
api.add_resource(PingView, '/ping', endpoint='bff_ping')
api.add_resource(OfferView, '/rf004/posts/<string:postId>/offers', endpoint='bff_create_offer')
api.add_resource(PostsView, '/rf005/posts/<string:postId>', endpoint='bff_query_post')
api.add_resource(PostsView, '/rf003/posts', endpoint='bff_create_post')



