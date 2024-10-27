from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus


class PingView(Resource):
    def get(self):
        return 'pong', HTTPStatus.OK