from flask_restful import Resource
from flask import Flask, request, jsonify
import base64
import json
from http import HTTPStatus
from ...models.card import Card,Status
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
from datetime import datetime,timezone
import re
import pytz
import logging
from dateutil import parser
import traceback
from ...apiClients.UserClient import UserClient
from ...apiClients.TrueNativeClient import TrueNativeClient
from ...models.verification_card import VerificationCard
import uuid
from ...apiClients.PubSubClient import publish_message




class CardView(Resource):
    """
    Esta clase corresponde al api de tarjetas de crédito
    Attributes:
        na
    """

   
    def card_request_is_valid(self):
        """
        Este método valida el request del post de credit card

        Args: 
            na
        Returns:
            na
        """
        try:
            if request.json["cardNumber"] is None:
                return False
            
            if request.json["cvv"] is None:
                return False
            
            if request.json["expirationDate"] is None:
                return False
            
            if request.json["cardHolderName"] is None:
                return False
            
            if not str(request.json["cardNumber"]).isdigit():
                return False
            
            if not str(request.json["cvv"]).isdigit():
                return False
            

            patternDate = re.compile(r'^\d{2}/\d{2}$')

            if not patternDate.match(str(request.json["expirationDate"])):
                return False
            

            if len(str(request.json["cardHolderName"]))<3:
                return False
        except Exception as e:
            return False
        return True


        

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
        



    def request_verify_card(self,transaction_identifier):
        """
        Este método permite realizar solicitud de verificación de una tarjeta
        Args:
            na
        Returns:
            response (VerificationCardResponse): respuesta de la verificación
        """
        true_native_client=TrueNativeClient()
        return true_native_client.registerCard(
            VerificationCard(
                    card_holder_name=request.json["cardHolderName"],
                    card_number=request.json["cardNumber"],
                    cvv=request.json["cvv"],
                    expiration_date=request.json["expirationDate"],
                    transaction_identifier=transaction_identifier
            )
        )
    

    def is_card_expired(self,year, month):
        '''
        este metodo permite determinar si una tarjeta ya venció
        Args:
            year (int): es el año
            month (int): es el mes
        Returns:
            bool
        '''
        current_date = datetime.now()
        current_year = int(str(current_date.year)[-2:])
        current_month = int(current_date.month)

        self.logger.info(f'evaluación de fechas current_date {current_date} current year {current_year} current_mont {current_month} year {year} month {month}')

        if int(year)<current_year:
            return True
        
        if int(year)==current_year and int(month)<current_month:
            return True
        
        return False

  


    


    @require_bearer_token
    def post(self):
        """
        Este método expone como api la creación de una tarjeta de crédito
        Args:
            request
        Returns:
            na
        """

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'post de tarjeta')

        unique_id = uuid.uuid4()
        transaction_identifier= str(unique_id)

        user=self.query_user_id()
        cardAlreadyExist=Card.query.filter_by(userId=user.get_id(), lastFourDigits=request.json["cardNumber"][-4:]).all()
        

        # the card already exist for de user
        if cardAlreadyExist:
            return ('', HTTPStatus.CONFLICT) 
        
       
        if not self.card_request_is_valid():
            return '', HTTPStatus.BAD_REQUEST
        
        '''
        salio todo bien entonces a crear la tarjeta
        1 verificar la tarjeta
        2 registrar la tarjeta
        '''

        response=self.request_verify_card(transaction_identifier)
        self.logger.info(f'el response de verificacion {response}')

        if not response.get_token():
            return {
                'no se obtuvo un token de verificación'
            }, HTTPStatus.PRECONDITION_FAILED
        
        self.logger.info(f'validando la fecha de expiración {request.json["expirationDate"]}')
        year, month = map(int, request.json["expirationDate"].split('/'))
        

        if self.is_card_expired(year, month):
            return '', HTTPStatus.PRECONDITION_FAILED
              
        new_card=Card(
            id=transaction_identifier,
            token=response.get_token(),
            ruv=response.get_ruv(),
            issuer=response.get_issuer(),
            userId=user.get_id(),
            lastFourDigits=request.json["cardNumber"][-4:],
            userEmail=user.get_email()
        )



    
        db.session.add(new_card)
        db.session.commit()

        self.logger.info(f'card creado {new_card}')

        self.logger.info(f'el ruv y el transaction identifier {response.get_ruv()} - {transaction_identifier}')

       

        return {
            "id": str(new_card.id),
            "userId":user.get_id(),
            "createdAt": new_card.createdAt.isoformat()
        }, HTTPStatus.CREATED
    



