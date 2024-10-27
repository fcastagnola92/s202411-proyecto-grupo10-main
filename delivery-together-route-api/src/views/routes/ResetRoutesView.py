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




class ResetRoutesView(Resource):
     
    def post(self):
        Route.query.delete()
        db.session.commit()
        return {
            "msg": "Todos los datos fueron eliminados"
        }, HTTPStatus.OK