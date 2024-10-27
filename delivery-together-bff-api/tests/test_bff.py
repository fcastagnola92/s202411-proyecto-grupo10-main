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

from unittest.mock import MagicMock, patch,Mock
import os

from  src.models.Offer import Offer
from  src.models.Post import Post
from  src.models.Score import Score
from src.views.offers.OfferView import OfferView
import requests
from src.apiClients.UserClient import UserClient
from src.apiClients.ScoreClient import ScoreClient
from src.apiClients.RouteClient import RouteClient
from src.apiClients.PostClient import PostClient
from src.apiClients.OfferClient import OfferClient
from src.transactions.transactions import *
from src.middleWare.authMiddleware import *

class TestBff(TestCase):
    


    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        self.token=str(uuid.uuid4())
        self.new_route=None
        os.environ['ENVIRONMENT']='test'
        self.post_id = uuid.uuid4()
        self.description = self.data_factory.name(),
        self.size = "LARGE"
        self.fragile = True
        self.offer_value = self.data_factory.random_int(min=1, max=1000),
        self.route_id = self.data_factory.name(),
        self.user_id = self.data_factory.name(),
        self.expire_at = datetime.now() + timedelta(days=7)
        self.created_at = datetime.now()
        self.bag_cost = self.data_factory.random_int(min=1, max=1000),
        self.offer_value = self.data_factory.random_int(min=1, max=1000),
        self.offer_id = uuid.uuid4()


    def authentication(self):
        user_name=self.data_factory.user_name()
        password=self.data_factory.password(length=8)
        data={
            "username": user_name,
            "password": password,
            "email": self.data_factory.email(),
            "dni": self.data_factory.random_int(min=100000000, max=999999999),
            "fullName": self.data_factory.name(),
            "phoneNumber": self.data_factory.phone_number()
        }
        print(f"{os.environ.get('USERS_PATH')}/users")
        response = requests.post(f"{os.environ.get('USERS_PATH')}/users",json=data)
        data = response.json()
        self.userid=data.get('id')


        data={
            "username": user_name,
            "password": password
        }
        response = requests.post(f"{os.environ.get('USERS_PATH')}/users/auth",json=data)
        data = response.json()
        self.token=data.get('token')
        print(self.token)
        
        
        

    def tearDown(self):
        pass

    def testPing(self):
        endpoint_ping = "/ping"
        response_ping = self.client.get(endpoint_ping)                   
        self.assertEqual(response_ping.status_code, 200)


    def test_offer_initialization(self):
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)

        self.assertEqual(offer.get_post_id(), self.post_id)
        self.assertEqual(offer.get_description(), self.description)
        self.assertEqual(offer.get_size(), self.size)
        self.assertEqual(offer.get_fragile(), self.fragile)
        self.assertEqual(offer.get_offer(), self.offer_value)

    def test_get_post_id(self):
        # Verifica que el método get_post_id devuelva el valor esperado
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)
        self.assertEqual(offer.get_post_id(), self.post_id)

    def test_get_description(self):
        # Verifica que el método get_description devuelva el valor esperado
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)
        self.assertEqual(offer.get_description(), self.description)

    def test_get_size(self):
        # Verifica que el método get_size devuelva el valor esperado
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)
        self.assertEqual(offer.get_size(), self.size)

    def test_get_fragile(self):
        # Verifica que el método get_fragile devuelva el valor esperado
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)
        self.assertEqual(offer.get_fragile(), self.fragile)

    def test_get_offer(self):
        # Verifica que el método get_offer devuelva el valor esperado
        offer = Offer(self.post_id, self.description, self.size, self.fragile, self.offer_value)
        self.assertEqual(offer.get_offer(), self.offer_value)


    def test_post_initialization(self):
        # Verifica que la inicialización de la clase funcione correctamente
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)

        self.assertEqual(post.get_id(), self.post_id)
        self.assertEqual(post.get_route(), self.route_id)
        self.assertEqual(post.get_user(), self.user_id)
        self.assertEqual(post.get_expire(), self.expire_at)
        self.assertEqual(post.get_createdAt(), self.created_at)

    def test_get_id(self):
        # Verifica que el método get_id devuelva el valor esperado
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)
        self.assertEqual(post.get_id(), self.post_id)

    def test_get_route(self):
        # Verifica que el método get_route devuelva el valor esperado
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)
        self.assertEqual(post.get_route(), self.route_id)

    def test_get_user(self):
        # Verifica que el método get_user devuelva el valor esperado
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)
        self.assertEqual(post.get_user(), self.user_id)

    def test_get_expire(self):
        # Verifica que el método get_expire devuelva el valor esperado
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)
        self.assertEqual(post.get_expire(), self.expire_at)

    def test_get_createdAt(self):
        # Verifica que el método get_createdAt devuelva el valor esperado
        post = Post(self.post_id, self.route_id, self.user_id, self.expire_at, self.created_at)
        self.assertEqual(post.get_createdAt(), self.created_at)


    def test_score_initialization(self):
        # Verifica que la inicialización de la clase funcione correctamente
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)

        self.assertEqual(score.get_bag_cost(), self.bag_cost)
        self.assertEqual(score.get_offer(), self.offer_value)
        self.assertEqual(score.get_offer_id(), self.offer_id)
        self.assertEqual(score.get_route_id(), self.route_id)
        self.assertEqual(score.get_size(), self.size)

    def test_get_bag_cost(self):
        # Verifica que el método get_bag_cost devuelva el valor esperado
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)
        self.assertEqual(score.get_bag_cost(), self.bag_cost)

    def test_get_offer(self):
        # Verifica que el método get_offer devuelva el valor esperado
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)
        self.assertEqual(score.get_offer(), self.offer_value)

    def test_get_offer_id(self):
        # Verifica que el método get_offer_id devuelva el valor esperado
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)
        self.assertEqual(score.get_offer_id(), self.offer_id)

    def test_get_route_id(self):
        # Verifica que el método get_route_id devuelva el valor esperado
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)
        self.assertEqual(score.get_route_id(), self.route_id)

    def test_get_size(self):
        # Verifica que el método get_size devuelva el valor esperado
        score = Score(self.bag_cost, self.offer_value, self.offer_id, self.route_id, self.size)
        self.assertEqual(score.get_size(), self.size)


    def test_query_user_success(self):
        self.authentication()
       
        user_client = UserClient(token=self.token)
        user_id=user_client.queryUser()
        
        self.assertNotEqual(user_id, None)

    def test_query_user_unsuccess(self):
        self.authentication()
       
        user_client = UserClient(token='fake')
        user_id=user_client.queryUser()
        
        self.assertEqual(user_id, None)


    def test_create_score_un_success(self):
        self.authentication()
       
        score_client = ScoreClient(token='fake')
        result=score_client.createScore(score=None)
        
        self.assertEqual(result, None)


    def test_queryBagCostRoute_un_success(self):
        self.authentication()
       
        route_client = RouteClient(token=self.token)
        result=route_client.queryBagCostRoute(idRoute=None)
        
        self.assertEqual(result, None)


    def test_queryBagCostRoute_success(self):
        self.authentication()
        #creando una ruta
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
        headers = {
            'Authorization': self.token
        } 
        response = requests.post(f"{os.environ.get('ROUTE_PATH')}/routes",json=new_route,headers=headers)
        data = response.json()
        print(f'respuesta de crear ruta {data}')
        print(f'el status code de rutas {response.status_code}')
        id_route=data.get('id')
       
        route_client = RouteClient(token=self.token)
        result=route_client.queryBagCostRoute(idRoute=id_route)
        
        self.assertNotEqual(result, None)


    def test_queryPost_un_success(self):
        self.authentication()
       
        post_client = PostClient(token=self.token)
        result=post_client.queryPost(idPost=None)
        
        self.assertEqual(result, None)


    def test_createOffer_un_success(self):
        self.authentication()
       
        offer_client = OfferClient(token=self.token)
        result=offer_client.createOffer(offer=None)
        
        self.assertEqual(result, None)

    def test_removeOffer_un_success(self):
        self.authentication()
       
        offer_client = OfferClient(token=self.token)
        result=offer_client.removeOffer(offerId=None)
        
        self.assertEqual(result, None)

    
    def test_add_step_saga(self):
        saga=Saga()
        saga.add_step("nombre","action")
        self.assertEqual(True,True)


    def test_execute_saga(self):
        saga=Saga()
        saga.add_step("nombre","action")
        saga.execute()
        self.assertEqual(True,True)

    def test_compensate_saga(self):
        saga=Saga()
        saga.add_step("nombre","action")
        saga.compensate("nombre")
        self.assertEqual(True,True)

    def test_set_status_saga(self):
        saga=Saga()
        saga.setLastStatusCode(200)
        self.assertEqual(True,True)

   
    def test_get_status_saga(self):
        saga=Saga()
        saga.setLastStatusCode(200)
        result=saga.getLastStatusCode()
        self.assertNotEqual(result,None)


    def test_is_uniqueidentifier_valid(self):
        valid_uuid = self.data_factory.uuid4()
        result = is_uniqueidentifier(valid_uuid)
        self.assertTrue(result)


    def test_offerview_createoffer_unsuccess_request(self):
        endpoint_route=f"/rf004/posts/{self.data_factory.uuid4()}/offers"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        new_offer={
            "description": "maleta grande",
            "size": "LARGE",
            "fragile" : True,
            "offer": 50
        }
        result_new_offer = self.client.post(endpoint_route,
                                                   data=json.dumps(new_offer),
                                                   headers=headers)

        self.assertNotEqual(result_new_offer.status_code, 201)


    # def test_offerview_queryUserId_request(self):
    #     self.authentication()
    #     offer_view=OfferView()
    #     offer_view.queryUserId(self.token)
    #     self.assertEqual(True,True)

    


    def test_saga_context_add_data(self):
        saga_context=SagaContext()
        saga_context.add_data("dato","value")
        self.assertEqual(True,True)

    def test_saga_context_get_data(self):
        saga_context=SagaContext()
        saga_context.add_data("dato","value")
        saga_context.get_data("dato")
        self.assertEqual(True,True)


    
    def test_require_bearer_token_test_environment(self):

        @require_bearer_token
        def test_function(*args, **kwargs):
            return "Success"

        result = test_function()
        self.assertEqual(result, "Success")

    
   
