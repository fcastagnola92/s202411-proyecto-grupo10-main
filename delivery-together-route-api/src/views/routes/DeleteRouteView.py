from flask_restful import Resource
from flask import Flask, request, jsonify
import base64
import json
from http import HTTPStatus
from ...models.route import Route
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
from datetime import datetime
import re




class DeleteRouteView(Resource):

    def is_uniqueidentifier(self,value):
        uuid_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        return bool(uuid_pattern.match(value))
     
    @require_bearer_token
    def delete(self, id):
        if id is not None and self.is_uniqueidentifier(id):
            route = Route.query.get(id)

            if route is None:
                return '', HTTPStatus.NOT_FOUND

            db.session.delete(route)
            db.session.commit()

            return {
                "msg": "el trayecto fue eliminado"
            }, HTTPStatus.OK

        else:
            return ('', HTTPStatus.BAD_REQUEST) 