from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
from ..models.Score import Score
import logging
class ScoreClient:
    """
    Esta clase representa un cliente de la api de score
    Attributes:
        base_url (string): la url del servicio score
        token (string): el token para autenticarse en el servicio
    """

    def __init__(self,token):
        """
        Constructor del cliente
        Args:
            token (string): el token para autenticarse en el servicio
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'iniciando cliente de score')
        self.base_url = os.environ.get('SCORE_PATH')
        self.token=token

    def createScore(self,score):
        """
        metodo para consumir la api de creación de score
        Args:
            score (Score): score a crearse
        Return:
           na
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            data={
                "bagCost": score.get_bag_cost(),
                "offer": score.get_offer(),
                "offerId": score.get_offer_id(),
                "routeId": score.get_route_id(),
                "size": score.get_size()
            }
            response = requests.post(self.base_url,json=data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    score=data.get('score')
                            
                    return score
                    
                else:
                    self.logger.info(f'error al crear la oferta')
                    return None
            else:
                self.logger.info(f"api de oferta responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con score: {str(e)}")
            return None

