from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.verification_card import VerificationCard
from ..models.verification_response import VerificationCardResponse

class TrueNativeClient:
    """
    Esta clase representa un cliente de la api truenative
    Attributes:
        base_url (string): la url del servicio publicaciones
        token (string): el token para autenticarse en el servicio
    """

    def __init__(self):
        """
        Constructor del cliente
        Args:
            na
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'iniciando cliente de true native')
        self.base_url = os.environ.get('NATIVE_PATH')
        self.token=os.environ.get('NATIVE_TOKEN')

    
    def registerCard(self,card):
        """
        metodo para consumir la api de creación de post
        Args:
            post (Post): post a crearse
        Return:
          new_post (Post)
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            } 
            data={
                "card": {
                    "cardNumber": card.get_card_number(),
                    "cvv": card.get_cvv(),
                    "expirationDate": card.get_expiration_date(),
                    "cardHolderName": card.get_card_holder_name(),
                },
                "transactionIdentifier": card.get_transaction_identifier()
            }
            self.logger.info(f'a llamar a true native {self.base_url}/native/cards   {data}')
            response = requests.post(f'{self.base_url}/native/cards',json=data, headers=headers)
            
            if response.status_code == 201:
                data = response.json()
                if data:
                    verification_response=VerificationCardResponse(ruv=data.get('RUV'),createdAt=data.get('createdAt'),issuer=data.get('issuer'),task_status=data.get('task_status'),token=data.get('token'),transactionIdentifier=data.get('transactionIdentifier'))
                    return verification_response
                    
                else:
                    self.logger.info(f'no hay datos en la respuesta de verificacióin {data}')
                    return None
            else:
                self.logger.info(f"api de verificación responde con error: {response.status_code}, {response}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con verificación: {str(e)}")
            return None
        