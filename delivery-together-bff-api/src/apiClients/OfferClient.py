from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
from ..models.Offer import Offer
import logging

class OfferClient:
    """
    Esta clase representa un cliente de la api de ofertas
    Attributes:
        base_url (string): la url del servicio ofertas
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
        self.logger.info(f'iniciando cliente de ofertas')
        self.base_url = os.environ.get('OFFER_PATH')
        self.token=token

    def createOffer(self,offer):
        """
        metodo para consumir la api de creación de publicaciones
        Args:
            offer (Offer): oferta a crearse
        Return:
           uniqueidentifier: id de la oferta
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            data={
                "postId": offer.get_post_id(),
                "description": offer.get_description(),
                "size": offer.get_size(),
                "fragile":  offer.get_fragile(),
                "offer": offer.get_offer(),
            }
            self.logger.info(f'llamando a la api de ofertas {self.base_url}/offers')
            response = requests.post(f'{self.base_url}/offers',json=data, headers=headers)
            self.logger.info('se llamó al api de ofertas')
            if response.status_code == 201:
                self.logger.info('se creó con éxito la oferta')
                data = response.json()
                if data:
                    idOffer=data.get('id')
                            
                    return idOffer
                    
                else:
                    self.logger.info(f'error al crear la oferta')
                    return None
            else:
                self.logger.info(f"api de oferta responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con offers: {str(e)}")
            return None
        


    def removeOffer(self,offerId):
        """
        metodo para consumir la api de eliminación de ofertas
        Args:
            offerId (uniqueidentifier): oferta a elminarse
        Return:
           na
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            
            response = requests.delete(f'{self.base_url}/offers/{offerId}', headers=headers)
            if response.status_code == 200:
                return True
            else:
                self.logger.info(f"api de eliminar oferta responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con offers: {str(e)}")
            return None
    

    def queryOffersByPost(self,postId):
        """
        metodo para consumir la api de consulta de ofertas por publicación
        Args:
            postId (uniqueidentifier): id de publicación
        Return:
            Offer[] arreglo de ofertas
        """
        Offers=[]
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'llamando a la consulta de ofertas {self.base_url}/offers?post={postId}')
            response = requests.get(f'{self.base_url}/offers?post={postId}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for item in data:
                        Offers.append(
                            Offer(
                                id=item.get('id'),
                                postId=item.get('postId'),
                                description=item.get('description'),
                                size=item.get('size'),
                                fragile=item.get('fragile'),
                                offer=item.get('offer'),
                                createdAt=item.get('createdAt'),
                                userId=item.get('userId')
                            )
                        )
                    return Offers
                    
                else:
                    self.logger.info(f'no se encontraron ofertas')
                    return Offers
            else:
                self.logger.info(f"api de ofertas responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con ofertas: {str(e)}")
            return None

