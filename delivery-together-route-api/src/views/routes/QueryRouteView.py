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




class QueryRouteView(Resource):

    def is_uniqueidentifier(self,value):
        uuid_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        return bool(uuid_pattern.match(value))
     
    @require_bearer_token
    def get(self, id):
        if id is not None and self.is_uniqueidentifier(id):
            route = Route.query.get(id)

            if route is None:
                return '', HTTPStatus.NOT_FOUND

            route_item = {
                'id': route.id,
                'flightId': route.flightId,
                'sourceAirportCode': route.sourceAirportCode,
                'sourceCountry': route.sourceCountry,
                'destinyAirportCode': route.destinyAirportCode,
                'destinyCountry': route.destinyCountry,
                'bagCost': route.bagCost,
                'plannedStartDate': route.plannedStartDate.isoformat(),
                'plannedEndDate': route.plannedEndDate.isoformat(),
                'createdAt': route.createdAt.isoformat()
            }

            return jsonify(route_item)
        else:
            return ('', HTTPStatus.BAD_REQUEST) 