from flask_restful import Resource
from flask import Flask, request, jsonify
import base64
import json
from http import HTTPStatus
from ...models.route import Route
from ...dataContext.sqlAlchemyContext import db
from functools import wraps
from ...middleWare.authMiddleware import *
from datetime import datetime,timezone
import re
import pytz
import logging
from dateutil import parser
import traceback





class RouteView(Resource):

    def is_uniqueidentifier(self,value):
        uuid_pattern = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        return bool(uuid_pattern.match(value))

    def validateEmptyFields(self,request):
        emptyFieldError=False
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('default')
        try:
            logger.info(f'vamos a leer los campos')
            flightId=request.json["flightId"]
            sourceAirportCode=request.json["sourceAirportCode"]
            sourceCountry=request.json["sourceCountry"]
            destinyAirportCode=request.json["destinyAirportCode"]
            destinyCountry=request.json["destinyCountry"]
            bagCost=request.json["bagCost"]
            plannedStartDate=request.json["plannedStartDate"]
            plannedEndDate=request.json["plannedEndDate"]
            logger.info(f'los leimos todos')
            if flightId is None:
                logger.info(f'1')
                emptyFieldError=True
            
            if sourceAirportCode is None:
                logger.info(f'2')
                emptyFieldError=True

            if sourceCountry is None:
                logger.info(f'3')
                emptyFieldError=True

            if destinyAirportCode is None:
                logger.info(f'4')
                emptyFieldError=True

            if destinyCountry is None:
                logger.info(f'5')
                emptyFieldError=True

            if bagCost is None:
                logger.info(f'6')
                emptyFieldError=True

            if plannedStartDate is None:
                logger.info(f'7')
                emptyFieldError=True

            if plannedEndDate is None:
                logger.info(f'8')
                emptyFieldError=True

        except Exception as e:
            emptyFieldError= True
            logger.info(f'error validando los campos {e}')
            logger.info(f'el stack trace {traceback.format_exc()}')
            

        return emptyFieldError
    

    def validateDatesRoute(self, plannedStartDate, plannedEndDate):
        invalidDates=False

        current_utc = datetime.utcnow()

        horario_utc = pytz.timezone('UTC')


        current_hour = current_utc.replace(tzinfo=horario_utc)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('default')

        try:
            logger.info('vamos don dateutil')
            if parser.parse(plannedStartDate)<current_hour:
                invalidDates=True

            if parser.parse(plannedEndDate)<current_hour:
                invalidDates=True


            if parser.parse(plannedEndDate)<=parser.parse(plannedStartDate):
                invalidDates=True

        except Exception as e:
            logger.error(f'error validando las fechas {e}')
            invalidDates=False

        return invalidDates

    
    @require_bearer_token
    def post(self):

        if self.validateEmptyFields(request):
            return ('', HTTPStatus.BAD_REQUEST) 
        
        routeAlreadyExist=Route.query.filter_by(flightId =request.json["flightId"]).all()

        # the route already exist
        if routeAlreadyExist:
            return ('', HTTPStatus.PRECONDITION_FAILED) 
        
       
        if self.validateDatesRoute(request.json["plannedStartDate"], request.json["plannedEndDate"]):
            return {
                "msg": "Las fechas del trayecto no son válidas"
            }, HTTPStatus.PRECONDITION_FAILED



        new_route=Route(
            flightId=request.json["flightId"],
            sourceAirportCode=request.json["sourceAirportCode"],
            sourceCountry=request.json["sourceCountry"],
            destinyAirportCode=request.json["destinyAirportCode"],
            destinyCountry=request.json["destinyCountry"],
            bagCost=request.json["bagCost"],
            plannedStartDate=request.json["plannedStartDate"],
            plannedEndDate=request.json["plannedEndDate"]
        )
        db.session.add(new_route)
        db.session.commit()


        return {
            "id": str(new_route.id),
            "createdAt": new_route.createdAt.isoformat()
        }, HTTPStatus.CREATED
    

    @require_bearer_token
    def get(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('default')

        flightIdParam=request.args.get('flight')

        logger.info(f'flight param: {flightIdParam}')



        routeList=[]
        queryResult=None

        if flightIdParam:
            queryResult=Route.query.filter_by(flightId = flightIdParam).all()
        else:
            queryResult=Route.query.all()

        for route in queryResult:
            routeItem={
                'id': route.id,
                'flightId': route.flightId,
                'sourceAirportCode': route.sourceAirportCode,
                'sourceCountry': route.sourceCountry,
                'destinyAirportCode': route.destinyAirportCode,
                'destinyCountry': route.destinyCountry,
                'bagCost': route.bagCost,
                'plannedStartDate': route.plannedStartDate.isoformat(),
                'plannedEndDate': route.plannedEndDate.isoformat(),
                'createdAt': route.createdAt.isoformat()
            }
            routeList.append(routeItem)
        
        return jsonify(routeList)
    

    
     
    @require_bearer_token
    def delete(self, id):
        if id is not None and self.is_uniqueidentifier(id):
            route = Route.query.get(id)

            if route is None:
                return '', HTTPStatus.NOT_FOUND

            db.session.delete(route)
            db.session.commit()

            return {
                "msg": "el trayecto fue eliminado"
            }, HTTPStatus.OK
        else:
            return ('', HTTPStatus.BAD_REQUEST) 
    
