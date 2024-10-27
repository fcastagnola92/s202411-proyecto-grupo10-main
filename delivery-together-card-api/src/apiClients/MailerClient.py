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

class MailerClient:
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
        self.logger.info(f'iniciando cliente de Mailer')
        self.base_url = os.environ.get('MAILER_PATH')

    
    def sendMail(self,to,subject,message ):
        """
        metodo para consumir la api de creación de post
        Args:
            to (string): destinatario
            subject (string): asunto
            message (string): el mensaje
        Return:
          na
        """
        try:
            headers = {
                'Content-Type': 'application/json',
            } 
            data={
                "to": to,
                "subject": subject,
                "message": message
            }

            self.logger.info(f'a llamar a mailer {self.base_url}/mailer/mail/send   {data}')
            response = requests.post(f'{self.base_url}/mailer/mail/send',json=data, headers=headers)
            if response.status_code == 200:
                self.logger.info(f"api mailer responde mail enviado con éxito {response.json()}")
                return
            else:
                self.logger.info(f"api de mailer responde con error: {response.status_code}, {response}")
                return
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con mailer: {str(e)}")
            return None
        