
from flask_restful import Resource, Api
from flask import Flask, request, json

from src import create_app
from .config.config import Config
from .dataContext.sqlAlchemyContext import db
from .views import PingView,RouteView,QueryRouteView,DeleteRouteView,ResetRoutesView
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
api.add_resource(PingView, '/routes/ping', endpoint='route_ping')
api.add_resource(RouteView, '/routes', endpoint='routes')
api.add_resource(QueryRouteView, '/routes/<string:id>', endpoint='route_by_id')
api.add_resource(DeleteRouteView, '/routes/<string:id>', endpoint='delete_route_by_id')
api.add_resource(ResetRoutesView, '/routes/reset', endpoint='route_reset')



