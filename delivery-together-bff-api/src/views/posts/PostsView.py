from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...middleWare.authMiddleware import *
from ...apiClients.PostClient import *
from ...apiClients.UserClient import *
from ...apiClients.OfferClient import *
from ...apiClients.ScoreClient import *
from ...apiClients.RouteClient import *
from ...models.Post import *
from datetime import datetime,timezone
import pytz
import logging
from dateutil import parser
from ...transactions.transactions import Saga, SagaError,SagaContext
from ...exceptions.aggregation_exception import Aggregation_Exception
import json

class PostsView(Resource):
    """
    Esta clase corresponde a una api de publicaciones
    Attributes:
        na
    """

    def queryPost(self,postId):
        """
        Este método consulta un post por el id

        Args: 
                postId (uniqueidentifier): id de la publicación.
        Returns:
            post (Post) 
        """
        postClient=PostClient(request.headers.get("Authorization"))
        post= postClient.queryPost(postId)
        if post is None:
            raise Aggregation_Exception("",HTTPStatus.NOT_FOUND)
        return post
    
    def queryRoute(self,routeId):
        """
        Este método consulta una ruta por el id

        Args: 
                routeId (uniqueidentifier): id de la ruta.
        Returns:
            ruta (Route) 
        """
        routeClient=RouteClient(request.headers.get("Authorization"))
        route=routeClient.queryRoute(routeId)
        return route
    
    def queryOffers(self, postId):
        """
        Este método consulta un ofertas por el id de post

        Args: 
                postId (uniqueidentifier): id de la publicación.
        Returns:
            offers[] (Offer) 
        """
        offerClient=OfferClient(request.headers.get("Authorization"))
        offers=offerClient.queryOffersByPost(postId)
        return offers
    
    def serialize_offer(self,obj):
        """
        Este método serializa un objeto oferta

        Args: 
                token (string): el token de autenticación
                score (score): un objeto tipo score
        Returns:
            na
        """
        if isinstance(obj, Offer):
            return obj.to_dict()
        raise TypeError("Object not serializable")
    
    def createScore(self,offerId,routeId,size,offerValue,bag_cost):
        """
        Este método crea un registro de score

        Args: 
                token (string): el token de autenticación
                score (score): un objeto tipo score
        Returns:
            na
        """
        scoreClient=ScoreClient(token=request.headers.get("Authorization"))
        score=Score(
             bagCost=bag_cost,
             offer=offerValue,
             offerId=offerId,
             routeId=routeId,
             size=size
        )
        score_result=scoreClient.createScore(score=score)
        if score_result is None:
            return 0
        else:
            return score_result
        

    def queryUserIdForQuery(self):
        """
        Este método permite consultar el id del usuario
        Args:
            na
        Returns:
            na
        """
        user_client=UserClient(token=request.headers.get("Authorization"))
        result= user_client.queryUser()
        if result:
            return result

    @require_bearer_token
    def get(self,postId):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'obteniendo una publicación...')
        try:
            self.logger.info(f'quering post...')
            post=self.queryPost(postId)
            #Si el usuario no es el dueño de la publicación se debe presentar un error. Solo el propietario debe ver la información de sus propias publicaciones.
            userId=self.queryUserIdForQuery()
            if userId!=post.userId:
                return '',HTTPStatus.FORBIDDEN
            self.logger.info(f'quering Route...')
            route=self.queryRoute(post.get_route())
            offers=self.queryOffers(postId)
            for item in offers:
                item.set_score(
                    self.createScore(
                        offerId=item.get_id(),
                        routeId=post.get_route(),
                        size=item.get_size(),
                        offerValue=item.get_offer(),
                        bag_cost=route.get_bag_cost()
                    )
                )
            offers_sorted = sorted(offers, key=lambda x: x.get_score(), reverse=True)
            offer_string=json.dumps(offers_sorted, default=self.serialize_offer)
            
            return {
                    "data": {
                        "id": post.get_id(),
                        "expireAt": post.get_expire(),
                        "route": {
                            "id": route.get_id(),
                            "flightId": route.get_flight_id(),
                            "origin": {
                                "airportCode": route.get_source_airport_code(),
                                "country": route.get_source_country(),
                            },
                            "destiny": {
                                "airportCode": route.get_destiny_airport_code(),
                                "country": route.get_destiny_country(),
                            },
                            "bagCost": route.get_bag_cost(),
                        },
                        "plannedStartDate": route.get_planned_start_date(),
                        "plannedEndDate": route.get_planned_end_date(),
                        "createdAt": post.get_createdAt(),
                        "offers": json.loads(offer_string)
                    }
                },HTTPStatus.OK
        except Aggregation_Exception as e:
            #return e.mensaje,e.status_code
            raise e
        except Exception as e:
            #return str(e) ,HTTPStatus.INTERNAL_SERVER_ERROR
            raise e


    def validateRequest(self):
        """
        Este método permite validar la solicitud
        Args:
            na
        """
 
        try:

            if request.json["flightId"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe proveer el id del vuelo")

            if request.json["expireAt"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe proveer la fecha de expiración")
            
            if request.json["plannedStartDate"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe indicar la fecha planeada de inicio")
            
            if request.json["plannedEndDate"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar la fecha planeada de fin")
            
            if request.json["bagCost"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar el costo del equipaje")
            
            if request.json["origin"]["airportCode"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar el codigo del aereopuerto origen")
            
            if request.json["origin"]["country"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar el pais del aereopuerto origen")
            
            if request.json["destiny"]["airportCode"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar el codigo del aereopuerto destino")
            
            if request.json["destiny"]["country"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se indicar el pais del aereopuerto destino")
            
           
        except Exception as e:
            self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
            raise Exception(e)

    def queryRoutebyFlight(self):
        """
        Este método consulta una ruta por el id

        Args: 
                routeId (uniqueidentifier): id de la ruta.
        Returns:
            ruta (Route) 
        """
        routeClient=RouteClient(request.headers.get("Authorization"))
        routes=routeClient.queryRouteByFlightId(request.json["flightId"])
        if routes:
            for item in routes:
                self.global_context.add_data("route",item)
        else:
            self.global_context.add_data("route",None)


    def createRoute(self):
        """
        Este método crea una ruta sino existe previamente
        Args: 
                na
        Returns:
            na
        """
        route=self.global_context.get_data("route")
        if route is None:
            #crear la ruta
            routeClient=RouteClient(request.headers.get("Authorization"))

            new_route=Route(destinyCountry=request.json["destiny"]["country"],
                    destinyAirportCode=request.json["destiny"]["airportCode"],
                    sourceCountry=request.json["origin"]["country"],
                    sourceAirportCode=request.json["origin"]["airportCode"],
                    bagCost=request.json["bagCost"],
                    plannedEndDate=request.json["plannedEndDate"],
                    plannedStartDate=request.json["plannedStartDate"],
                    flightId=request.json["flightId"],
                    id=None
                )
    
            route_id=routeClient.createRoute(
                new_route
            )
            new_route.id=route_id
            self.global_context.add_data("route",new_route)
        else:
            self.global_context.add_data("route",route)



    def removeRoute(self):
        """
        Este método eliminar un registro de Ruta

        Args: 
            na
        Returns:
            na
        """
        
        route=self.global_context.get_data("route")
        routeId=route.get_id()
        self.logger.info(f'se va borrar la ruta {routeId}')
        

        route_client=RouteClient(request.headers.get("Authorization"))
        route_client.removeRoute(routeId)





        

    def queryUserId(self):
        """
        Este método permite consultar el id del usuario
        Args:
            token (string): token de la petición
        Returns:
            na
        """
        user_client=UserClient(request.headers.get("Authorization"))
        result= user_client.queryUser()
        if result:
            self.global_context.add_data("userId",result)
        else:
            raise Exception("no se obtuvo el usuario")
        

    def validatePostDates(self):
        """
        Este método permite validar las fechas de la publicación
        Args:
            na
        Returns:
            na
        """
        current_utc = datetime.utcnow()
        horario_utc = pytz.timezone('UTC')
        current_hour = current_utc.replace(tzinfo=horario_utc)
        if parser.parse(request.json["plannedStartDate"])<current_hour:
            self.logger.info('La fecha inicio está en el pasado')
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception('Las fechas del trayecto no son válidas')

        if parser.parse(request.json["plannedEndDate"])<current_hour:
            self.logger.info('La fecha fin está en el pasado')
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception('Las fechas del trayecto no son válidas')
        
        if parser.parse(request.json["expireAt"])<current_hour:
            self.logger.info('La fecha expiración está en el pasado')
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception('La fecha expiración no es válida')


        if parser.parse(request.json["plannedEndDate"])<=parser.parse(request.json["plannedStartDate"]):
            self.logger.info('La fecha fin es menor que la fecha inicio')
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception('Las fechas del trayecto no son válidas')
        
        if parser.parse(request.json["expireAt"])>parser.parse(request.json["plannedStartDate"]):
            self.logger.info('La fecha fin es menor que la fecha inicio')
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception('Las fechas del trayecto no son válidas')
        


    def validatePostInRoute(self):
        """
        Este método permite validar si es ya existe una publicación de la misma ruta
        Args:
            na
        Returns:
            na
        """
        post_client=PostClient(request.headers.get("Authorization"))
        result= post_client.queryMyPosts()
        route=self.global_context.get_data("route")
        if result:
            for item in result:
                if item.get_route()==route.get_id():
                    self.logger.info('la ruta ya fue registrada en una publicación del usuario')
                    raise Exception(f"la ruta ya fue registrada en una publicación del usuario")


    def createPost(self):
        """
        Este método crea una post sino existe previamente
        Args: 
            na
        Returns:
            na
        """
        route=self.global_context.get_data("route")
        post_client=PostClient(request.headers.get("Authorization"))
        post=post_client.createPost(
            Post(
                id=None,
                routeId=route.get_id(),
                userId=None,
                expireAt=request.json["expireAt"],
                createdAt=None 
            )
        )

        if post:
            self.global_context.add_data("newPost",post)
        else:
            self.logger.info(f'no fue posible crear el post')
            raise Exception("no fue posible crear el post")



    def removePost(self):
        """
        Este método eliminar un registro de Post

        Args: 
            na
        Returns:
            na
        """
        post=self.global_context.get_data("newPost")
        post_client=PostClient(request.headers.get("Authorization"))
        post_client.removePost(post.get_id())
        





    # Solo un usuario autenticado puede realizar esta operación.
    @require_bearer_token
    def post(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'recibiendo peticion de creación de post en bff')
        try:
            self.saga = Saga()
            self.saga.setLastStatusCode(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.global_context = SagaContext()
            #validando todos los campos
            self.saga.add_step("validar request", self.validateRequest())
            # El usuario brinda los datos de la publicación y el trayecto que hará.
            # Se valida si el trayecto ya existe o no, 
            self.saga.add_step("validando que exista la ruta",self.queryRoutebyFlight())
            #sino existe se crea con los valores indicados y se usa ese para la creación de la publicación, si ya existe se descartan los datos brindados y se usa el que está almacenado.
            self.saga.add_step("crear la ruta",self.createRoute())
            # La publicación queda asociada al usuario de la sesión.
            self.saga.add_step("consultando el usuario en sesión", self.queryUserId())
            # La plataforma solo permite crear publicaciones cuando la fecha de inicio de viaje es en el futuro.
            # La plataforma solo permite crear publicaciones cuando la fecha de expiración de la publicación es posterior a la fecha actual 
            #y anterior o igual a la fecha de inicio de viaje.
            self.saga.add_step("validando fechas de la publicación",self.validatePostDates(),self.removeRoute())
            # Si el usuario ya tiene otra publicación para el mismo trayecto se rechaza la creación.
            self.saga.add_step("validando que la publicación ya no se haya hecho antes por el mismo usuario",self.validatePostInRoute())
            # Crear post
            self.saga.add_step("creando el nuevo post",self.createPost())

            
            
            try:
                # En cualquier caso de error la información al finalizar debe ser consistente.
                self.saga.execute()
                self.logger.info("Saga completado exitosamente!")

                #obtener el user id
                user_id=self.global_context.get_data("userId")
                post=self.global_context.get_data("newPost")
                route=self.global_context.get_data("route")

                self.logger.info('armando la respuesta')
                return {
                    "data": {
                    "id": post.get_id(),
                    "userId": user_id,
                    "createdAt": post.get_createdAt(),
                    "expireAt": request.json["expireAt"],
                    "route": {
                        "id": route.get_id(),
                        "createdAt": post.get_createdAt(),
                    }
                    },
                    "msg": "Publicación creada con éxito"
                },HTTPStatus.CREATED


            except SagaError as e:
                self.logger.info(f"Error durante la ejecución del Saga: {str(e)}")

                return {"msg":str(e)}, self.saga.getLastStatusCode()
                #raise e

        except Exception as e:
            self.logger.info(f"Error durante la ejecución de la Saga: {str(e)}")
            return {"msg":str(e)}, self.saga.getLastStatusCode()
        
            #raise e

        




