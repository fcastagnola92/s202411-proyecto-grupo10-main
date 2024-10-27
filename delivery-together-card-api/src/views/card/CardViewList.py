from flask_restful import Resource
from flask import Flask, request, jsonify
from http import HTTPStatus
from ...models.card import Card,Status,Issuer
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
from datetime import datetime,timezone
from dateutil import parser
from ...apiClients.UserClient import UserClient
import logging
import json

class CardListView(Resource):
    
    def query_user_id(self):
        """
        Este método permite consultar el id del usuario
        Args:
            token (string): token de la petición
        Returns:
            na
        """
        user_client=UserClient(request.headers.get("Authorization"))
        return user_client.queryUser()
    
  
    @require_bearer_token
    def get(self):       
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'get tarjetas list')
        user=self.query_user_id()

        # Consulta las tarjetas de crédito del usuario
        self.logger.info(f'consultando las tarjetas de {user.get_id()}')
        user_cards = Card.query.filter_by(userId=user.get_id()).all()
        self.logger.info(f'tarjetas encontradas {user_cards}')

        # Construye la respuesta JSON
        cards_list = []

       
        

            
        for card in user_cards:
            update_date=None
            if card.updateAt:
                update_date=card.updateAt.isoformat()
            card_info = {
                'id': str(card.id),
                'token': card.token,  
                'userId': card.userId,
                'lastFourDigits': card.lastFourDigits,
                'issuer': card.issuer.value,
                'status': card.status.value,
                'createdAt': card.createdAt.isoformat(),
                'updatedAt': update_date
            }
            cards_list.append(card_info)



        return jsonify(cards_list)