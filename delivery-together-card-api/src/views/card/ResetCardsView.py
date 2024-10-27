
from flask_restful import Resource
from flask import Flask, request, jsonify
import base64
import json
from http import HTTPStatus
from ...models.card import Card
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
import logging




class ResetCardsView(Resource):
     
    def post(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'reset de tarjeta')
        try:
            Card.query.delete()
            db.session.commit()
            return {
                "msg": "Todos los datos fueron eliminados"
            }, HTTPStatus.OK
        except Exception as e:
            self.logger.info(f'error al resetear la tarjeta {e}')
