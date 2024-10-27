from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.user import User
class UserClient:
    """
    Esta clase representa un cliente de la api de usuarios
    Attributes:
        base_url (string): la url del servicio usuarios
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
        self.logger.info(f'iniciando cliente de usuarios')
        self.base_url = os.environ.get('USERS_PATH')
        self.token=token
        self.logger.info(f'el token recibido {token}')

    def queryUser(self):
        """
        metodo para consumir la api de consulta de usuario
        Args:
            na
        Return:
            id (uniqueidentifier): id del usuario
        """
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'llamando a usuarios {self.base_url}/users/me')
            response = requests.get(f'{self.base_url}/users/me', headers=headers)
            if response.status_code == 200:
                
                data = response.json()
                if data:
                    user=User(data.get('id'),data.get('email'))
                    return user
                    
                else:
                    self.logger.info(f'no retorno datos el api del usuario')
                    return None
            else:
                self.logger.info(f"api de usuarios responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con usuarios: {str(e)}")
            return None

