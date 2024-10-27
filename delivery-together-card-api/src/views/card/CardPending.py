from flask_restful import Resource
from flask import Flask, request, jsonify
from http import HTTPStatus
from ...models.card import Card,Status
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
from datetime import datetime,timezone
from dateutil import parser
from ...apiClients.UserClient import UserClient
import logging
from ...apiClients.PubSubClient import publish_message
import os

class CardPendingView(Resource):
    
    
    def get(self):       
        self.logger = logging.getLogger('default')
        self.logger.info(f'obtener tarjetas por consultar el status')

        # Consulta las tarjetas de crédito del usuario
        user_cards = Card.query.filter_by(status=Status.POR_VERIFICAR).all()
        self.logger.info(f'los cards por verificar {user_cards}')

        
        '''
        publicando en la cola
        '''
        for item in user_cards:
            try:
                message = {
                    'ruv':item.ruv
                }
                publish_message(os.environ.get('PROJECT_ID'), os.environ.get('TOPIC'),message)

            except Exception as ex:
                self.logger.info(f'No se publicó este ruv {item.ruv} error: {ex}')

       

        return 'ok', HTTPStatus.OK