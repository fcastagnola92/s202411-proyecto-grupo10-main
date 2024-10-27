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
from ...apiClients.MailerClient import MailerClient
from ...models.verification_card import VerificationCard
import uuid




class UpdateCardView(Resource):
    """
    Esta clase corresponde al api para actualizar tarjetas de crédito
    Attributes:
        na
    """

    def serialize_card(self,obj):
        """
        Este método serializa un objeto 

        Args: 
                token (string): el token de autenticación
                score (score): un objeto tipo score
        Returns:
            na
        """
        if isinstance(obj, Card):
            return obj.to_dict()
        raise TypeError("Object not serializable")
    
    def send_email(self,to, subject,message):
        """
        Este método permite enviar un correo de confirmación de respuesta de la verificación
        Args:
            na
        Returns:
            na
        """
        mailerClient=MailerClient()
        mailerClient.sendMail(to,subject,message)

    def put(self,id_card):
        """
        Este método expone como api la actualización del estado de la tarjeta de crédito
        Args:
            request
        Returns:
            na
        """

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'put de status de tarjeta ruv:{request.json["RUV"]} id:{request.json["transactionIdentifier"]}')
        card = db.session.query(Card).filter(Card.ruv==request.json["RUV"], Card.id==request.json["transactionIdentifier"]).first()
        if card:
            self.logger.info(f'card encontrado ')
            card.set_status(request.json["status"])
            self.logger.info(f'status asignado {card.status}')
            card.set_updateDate(datetime.now())
            db.session.commit()
            self.logger.info(f'registro actualizado de cards')

            self.logger.info(f'enviando email a {card.userEmail}')
            '''
            Indiferente del resultado del proceso, el usuario dueño de la tarjeta debe ser notificado por medio de correo electrónico el resultado de la inscripción de la tarjeta. 
            El mensaje debe contener el resultado del proceso con los datos básicos de la tarjeta que está almacenada en la base de datos, 
            y el RUV generado por el tercero.
            '''
            self.send_email(card.userEmail,'Resultado de verificación',f'Su tarjeta terminada en {card.lastFourDigits} fue {card.status} se indica a continuación el número único de verificación {card.ruv}')
            
            return f'registro actualizado con éxito {card.id} {str(card.status)}',HTTPStatus.OK
        else:
            self.logger.info(f'card no encontrado {request.json["RUV"]} - {request.json["transactionIdentifier"]}')
            return 'no encontrado',HTTPStatus.NOT_FOUND
