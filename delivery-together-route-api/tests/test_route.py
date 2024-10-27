import json
import hashlib
from unittest import TestCase
from http import HTTPStatus
import random

from faker import Faker
from faker.generator import random
from src.app import app
import uuid
from datetime import datetime, timedelta
from src.models.route import Route
from src.dataContext.sqlAlchemyContext import db

from src.views.routes.RouteView import RouteView
from src.views.routes.QueryRouteView import QueryRouteView
from unittest.mock import MagicMock, patch
import os

class TestRoute(TestCase):
    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.token=str(uuid.uuid4())
        self.new_route=None
        os.environ['ENVIRONMENT']='test'

    def tearDown(self):
        pass

    def testPing(self):
        endpoint_ping = "/routes/ping"
        response_ping = self.client.get(endpoint_ping)                   
        self.assertEqual(response_ping.status_code, 200)


    def testCreateRoute(self):

        flightId=self.data_factory.name()
        sourceAirportCode=self.data_factory.name()
        sourceCountry=self.data_factory.name()
        destinyAirportCode=self.data_factory.name()
        destinyCountry=self.data_factory.name()
        bagCost=round(random.uniform(10, 1000), 2)
        plannedStartDate= (datetime.now()+ timedelta(days=1)).isoformat()
        plannedEndDate=(datetime.now()+ timedelta(days=2)).isoformat()

        new_route = {
            "flightId": flightId,
            "sourceAirportCode": sourceAirportCode,
            "sourceCountry": sourceCountry,
            "destinyAirportCode": destinyAirportCode,
            "destinyCountry": destinyCountry,
            "bagCost": bagCost,
            "plannedStartDate": plannedStartDate,
            "plannedEndDate": plannedEndDate
        }

        endpoint_route="/routes"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        result_new_route = self.client.post(endpoint_route,
                                                   data=json.dumps(new_route),
                                                   headers=headers)
        data_response = json.loads(result_new_route.get_data())
        self.new_route=data_response['id']
        self.assertEqual(result_new_route.status_code, 201)


    def test_is_uniqueidentifier_valid(self):
        with app.app_context():
            route_view = RouteView()
            valid_uuid = self.data_factory.uuid4()
            result = route_view.is_uniqueidentifier(valid_uuid)
            self.assertTrue(result)


    def test_get_route_without_flightId(self):
        end_point_routes = "/routes"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        response_routes = self.client.get(end_point_routes,headers=headers)                   
        self.assertEqual(response_routes.status_code, 200)


    def test_delete_route(self):
         
        flightId=self.data_factory.name()
        sourceAirportCode=self.data_factory.name()
        sourceCountry=self.data_factory.name()
        destinyAirportCode=self.data_factory.name()
        destinyCountry=self.data_factory.name()
        bagCost=round(random.uniform(10, 1000), 2)
        plannedStartDate= (datetime.now()+ timedelta(days=1)).isoformat()
        plannedEndDate=(datetime.now()+ timedelta(days=2)).isoformat()

        new_route=Route(
            flightId=flightId,
            sourceAirportCode=sourceAirportCode,
            sourceCountry=sourceCountry,
            destinyAirportCode=destinyAirportCode,
            destinyCountry=destinyCountry,
            bagCost=bagCost,
            plannedStartDate=plannedStartDate,
            plannedEndDate=plannedEndDate
        )
        db.session.add(new_route)
        db.session.commit()
        end_point_routes = '/routes/'+str(new_route.id)
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        response_routes = self.client.delete(end_point_routes,headers=headers)                   
        self.assertEqual(response_routes.status_code, 200)


    def test_get_route_with_flightId(self):

        flightId=self.data_factory.name()
        sourceAirportCode=self.data_factory.name()
        sourceCountry=self.data_factory.name()
        destinyAirportCode=self.data_factory.name()
        destinyCountry=self.data_factory.name()
        bagCost=round(random.uniform(10, 1000), 2)
        plannedStartDate= (datetime.now()+ timedelta(days=1)).isoformat()
        plannedEndDate=(datetime.now()+ timedelta(days=2)).isoformat()

        new_route=Route(
            flightId=flightId,
            sourceAirportCode=sourceAirportCode,
            sourceCountry=sourceCountry,
            destinyAirportCode=destinyAirportCode,
            destinyCountry=destinyCountry,
            bagCost=bagCost,
            plannedStartDate=plannedStartDate,
            plannedEndDate=plannedEndDate
        )
        db.session.add(new_route)
        db.session.commit()

        end_point_routes = "/routes?flight="+new_route.flightId
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        response_routes = self.client.get(end_point_routes,headers=headers)                   
        self.assertEqual(response_routes.status_code, 200)



    def test_is_uniqueidentifier_query_valid(self):
        with app.app_context():
            route_view = QueryRouteView()
            valid_uuid = self.data_factory.uuid4()
            result = route_view.is_uniqueidentifier(valid_uuid)
            self.assertTrue(result)


    def test_get_route_by_id(self):

        flightId=self.data_factory.name()
        sourceAirportCode=self.data_factory.name()
        sourceCountry=self.data_factory.name()
        destinyAirportCode=self.data_factory.name()
        destinyCountry=self.data_factory.name()
        bagCost=round(random.uniform(10, 1000), 2)
        plannedStartDate= (datetime.now()+ timedelta(days=1)).isoformat()
        plannedEndDate=(datetime.now()+ timedelta(days=2)).isoformat()

        new_route=Route(
            flightId=flightId,
            sourceAirportCode=sourceAirportCode,
            sourceCountry=sourceCountry,
            destinyAirportCode=destinyAirportCode,
            destinyCountry=destinyCountry,
            bagCost=bagCost,
            plannedStartDate=plannedStartDate,
            plannedEndDate=plannedEndDate
        )
        db.session.add(new_route)
        db.session.commit()

        end_point_routes = "/routes/"+str(new_route.id)
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        response_routes = self.client.get(end_point_routes,headers=headers)                   
        self.assertEqual(response_routes.status_code, 200)



    
    def test_reset_database(self):

        

        endpoint_route="/routes/reset"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        result_reset_database = self.client.post(endpoint_route,
                                                   headers=headers)
        self.assertEqual(result_reset_database.status_code, 200)



    def test_validateEmptyFields_all_fields_present(self):
        request_mock = MagicMock()

        flightId=self.data_factory.name()
        sourceAirportCode=self.data_factory.name()
        sourceCountry=self.data_factory.name()
        destinyAirportCode=self.data_factory.name()
        destinyCountry=self.data_factory.name()
        bagCost=round(random.uniform(10, 1000), 2)
        plannedStartDate= (datetime.now()+ timedelta(days=1)).isoformat()
        plannedEndDate=(datetime.now()+ timedelta(days=2)).isoformat()

        route_view = RouteView()
        request_mock.json = {
            "flightId": flightId,
            "sourceAirportCode": sourceAirportCode,
            "sourceCountry": sourceCountry,
            "destinyAirportCode": destinyAirportCode,
            "destinyCountry": destinyCountry,
            "bagCost": bagCost,
            "plannedStartDate": plannedStartDate,
            "plannedEndDate": plannedEndDate
        }

        result = route_view.validateEmptyFields(request_mock)

        self.assertFalse(result)





        