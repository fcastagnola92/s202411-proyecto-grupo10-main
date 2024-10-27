from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.Route import Route
class RouteClient:
    """
    Esta clase representa un cliente de la api de rutas
    Attributes:
        base_url (string): la url del servicio rutas
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
        self.logger.info(f'iniciando cliente de Rutas')
        self.base_url = os.environ.get('ROUTE_PATH')
        self.token=token

    def queryBagCostRoute(self,idRoute):
        """
        metodo para consumir la api de consulta de ruta
        Args:
            idRoute (uniqueidentifier): identificador de la ruta
        Return:
            long: costo de la maleta
        """
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'llamando a la consulta de rutas {self.base_url}/routes/{idRoute}')
            response = requests.get(f'{self.base_url}/routes/{idRoute}', headers=headers)
            if response.status_code == 200:
                
                data = response.json()
                if data:
                    return data.get('bagCost')
                    
                else:
                    self.logger.info(f'la ruta no fue encontrada')
                    return None
            else:
                self.logger.info(f"api de rutas responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con rutas bagcost: {str(e)}")
            return None
        


    def queryRoute(self,idRoute):
        """
        metodo para consumir la api de consulta de ruta
        Args:
            idRoute (uniqueidentifier): identificador de la ruta
        Return:
            Route objeto ruta
        """
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'llamando a la consulta de rutas {self.base_url}/routes/{idRoute}')
            response = requests.get(f'{self.base_url}/routes/{idRoute}', headers=headers)
            if response.status_code == 200:
                
                data = response.json()
                if data:
                    return Route(
                        id=data.get('id'),
                        flightId=data.get('flightId'),
                        sourceAirportCode=data.get('sourceAirportCode'),
                        sourceCountry=data.get('sourceCountry'),
                        destinyAirportCode=data.get('destinyAirportCode'),
                        destinyCountry=data.get('destinyCountry'),
                        bagCost=data.get('bagCost'),
                        plannedStartDate=data.get('plannedStartDate'),
                        plannedEndDate=data.get('plannedEndDate')
                    )
                    
                else:
                    self.logger.info(f'la ruta no fue encontrada')
                    return None
            else:
                self.logger.info(f"api de rutas responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con rutas queryroute: {str(e)}")
            return None
        

    def queryRouteByFlightId(self,flightId):
        """
        metodo para consumir la api de consulta de ruta por id de vuelo
        Args:
            flightId (str): identificador de un vuelo
        Return:
            Route objeto ruta
        """
        Routes =[]
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'llamando a la consulta de rutas por vuelo {self.base_url}/routes?flight={flightId}')
            response = requests.get(f'{self.base_url}/routes?flight={flightId}', headers=headers)
            if response.status_code == 200:
                
                data = response.json()
                if data:
                    for item in data:
                        Routes.append(
                            Route(
                                id=item.get('id'),
                                flightId=item.get('flightId'),
                                sourceAirportCode=item.get('sourceAirportCode'),
                                sourceCountry=item.get('sourceCountry'),
                                destinyAirportCode=item.get('destinyAirportCode'),
                                destinyCountry=item.get('destinyCountry'),
                                bagCost=item.get('bagCost'),
                                plannedStartDate=item.get('plannedStartDate'),
                                plannedEndDate=item.get('plannedEndDate')
                            )
                        )
                    return Routes
                    
                else:
                    self.logger.info(f'la ruta no fue encontrada')
                    return None
            else:
                self.logger.info(f"api de rutas responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con rutas queryRouteByFlightId: {str(e)}")
            return None
        


    def createRoute(self,route):
        """
        metodo para consumir la api de creación de ruta
        Args:
            route (Route): ruta a crearse
        Return:
           id ruta creada
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            data={
                "flightId": route.get_flight_id(),
                "sourceAirportCode": route.get_source_airport_code(),
                "sourceCountry": route.get_source_country(),
                "destinyAirportCode": route.get_destiny_airport_code(),
                "destinyCountry": route.get_destiny_country(),
                "bagCost": route.get_bag_cost(),
                "plannedStartDate": route.get_planned_start_date(),
                "plannedEndDate": route.get_planned_end_date(),
            }
            response = requests.post(f'{self.base_url}/routes',json=data, headers=headers)
            if response.status_code == 201:
                data = response.json()
                if data:
                    return data.get('id')
                    
                else:
                    self.logger.info(f'error al crear la ruta')
                    return None
            else:
                self.logger.info(f"api de ruta responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con ruta createRoute: {str(e)}")
            return None
        

    def removeRoute(self,routeId):
        """
        metodo para consumir la api de eliminación de rutas
        Args:
            routeId (uniqueidentifier): ruta a elminarse
        Return:
           na
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            self.logger.info(f'borrando la ruta {routeId}  {self.base_url}/routes/{routeId}')
            response = requests.delete(f'{self.base_url}/routes/{routeId}', headers=headers)
            if response.status_code == 200:
                return True
            else:
                self.logger.info(f"api de eliminar ruta responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con rutas removeRoute: {str(e)}")
            return None

