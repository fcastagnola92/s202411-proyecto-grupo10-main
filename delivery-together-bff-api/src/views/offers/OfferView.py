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


class OfferView(Resource):
    """
    Esta clase representa corresponde a una api de ofertas
    Attributes:
        global_context (SagaContext): contexto de la saga para controlar los datos de los pasos
    """

    
    def validateRequest(self,postId,request):
        """
        Este método permite validar la solicitud
        Args:
            request (request): el objeto request para validarse.
            idPost (int): id de la publicación.
        """
        try:
            if postId is  None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe proveer una publicación")

            if request.json["description"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe proveer una publicación")

            if request.json["size"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe proveer el tamaño")
            
            if request.json["fragile"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe indicar si el paquete es frágil o no")
            
            if request.json["offer"] is None:
                self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
                raise Exception("Se debe el valor de la oferta")
            
            if request.json["size"]!='LARGE' and request.json["size"]!='MEDIUM' and request.json["size"]!='SMALL':
                raise Exception("Se debe suministrar el tamaño que puede ser MEDIMUM, LARGE o SMALL")
            
            if isinstance(request.json["fragile"], bool)==False:
                raise Exception("El valor de fragíl debe ser un valor booleano")
            

            if isinstance(request.json["offer"], (int, float))==False:
                raise Exception("El valor de la oferta debe ser numérico")
        except Exception as e:
            self.saga.setLastStatusCode(HTTPStatus.BAD_REQUEST)
            raise Exception(e)
        


    def validatePost(self,request,idPost):
        """
        Este método valida que el post exista 

        Args: 
                idPost (int): id de la publicación.
                request (request): solicitud
        Returns:
            na
        """
        
        postClient=PostClient(request.headers.get("Authorization"))
        post= postClient.queryPost(idPost)
        if post:
            self.global_context.add_data("post",post)
        else:
            self.saga.setLastStatusCode(HTTPStatus.NOT_FOUND)
            raise Exception("el post no existe")
    

    def validatePostExpiration(self):
        """
        Este método permite validar si la publicación no ha expirado
        Args:
            na
        """
        post=self.global_context.get_data("post")
        current_utc = datetime.utcnow()
        if parser.parse(post.expireAt).replace(tzinfo=timezone.utc)<current_utc:
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception("la publicación expiró")
        

    def queryUserId(self, token):
        """
        Este método permite consultar el id del usuario
        Args:
            token (string): token de la petición
        Returns:
            na
        """
        user_client=UserClient(token)
        result= user_client.queryUser()
        if result:
            self.global_context.add_data("userId",result)
        else:
            raise Exception("no se obtuvo el usuario")
            

    def validateUserCreator(self):
        """
        Este método permite consultar el id del usuario
        Args:
            na
        """
        post=self.global_context.get_data("post")
        userId=self.global_context.get_data("userId")
        self.logger.info(f'usuario del post {post.get_user()} usuario de la autenticación {userId}')
        if post.get_user()==userId:
            self.saga.setLastStatusCode(HTTPStatus.PRECONDITION_FAILED)
            raise Exception("Se está intentando ofertar sobre una publicación del mismo usuario")
        

    def createOffer(self,request):
        """
        Este método crea una oferta

        Args: 
                request (request): solicitud
        Returns:
            objeto  json de retorno
        """
        offerClient=OfferClient(token=request.headers.get("Authorization"))
        post=self.global_context.get_data("post")
        offer=Offer(post.get_id(),
                    request.json["description"],
                    request.json["size"],
                    request.json["fragile"],
                    request.json["offer"])
        offer_id=offerClient.createOffer(offer=offer)
        if offer_id is None:
            raise Exception("Error al crear la oferta")
        self.global_context.add_data("offerCreated",offer_id)
        self.logger.info(f'se creó la oferta {offer_id}')
        


    def createScore(self,request):
        """
        Este método crea un registro de score

        Args: 
                token (string): el token de autenticación
                score (score): un objeto tipo score
        Returns:
            na
        """
        scoreClient=ScoreClient(token=request.headers.get("Authorization"))
        offerId=self.global_context.get_data("offerCreated")
        post=self.global_context.get_data("post")
        bag_cost=self.global_context.get_data("bag_cost")
        score=Score(
             bagCost=bag_cost,
             offer=request.json["offer"] ,
             offerId=offerId,
             routeId=post.get_route(),
             size=request.json["size"]
        )
        score_result=scoreClient.createScore(score=score)
        if score_result is None:
            #raise Exception("el score no fue obtenido")
            self.global_context.add_data("score_result",0)
        else:
            self.global_context.add_data("score_result",score_result)


    
    def removeOffer(self,request):
        """
        Este método eliminar un registro de offer

        Args: 
                token (string): el token de autenticación
                offerId (uniqueidentifier): id de la oferta
        Returns:
            na
        """
        offerId=self.global_context.get_data("offerCreated")
        offer_client=OfferClient(request.headers.get("Authorization"))
        offer_client.removeOffer(offerId=offerId)


    def queryRoute(self,request):
        """
        Este método consulta una ruta

        Args: 
                request (request): la solicitud enviada.
        Returns:
            na
        """
        #obtener la ruta
        post=self.global_context.get_data("post")
        print(post.get_route())
        print(post.get_id())
        route_client=RouteClient(token=request.headers.get("Authorization"))
        bag_cost=route_client.queryBagCostRoute(post.get_route())
        if bag_cost is None:
            #raise Exception(f"no se pudo obtener el costo de la maleta para la ruta {post.get_route()}")
            bag_cost=0
        self.global_context.add_data("bag_cost",bag_cost)
        self.logger.info(f'el costo de la maleta es {bag_cost}')
        
        


        

    

    # Solo un usuario autenticado puede realizar esta operación.
    @require_bearer_token
    def post(self,postId):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'recibiendo peticion de para offer en bff {postId}')
        try:
            self.saga = Saga()
            self.saga.setLastStatusCode(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.global_context = SagaContext()
            # validando que los endpoints estén disponibles
            # El usuario brinda la información de la oferta que desea hacer y el identificador de la publicación a la que se realiza.
            self.saga.add_step("validar request", self.validateRequest(postId,request))
            # Se valida que la publicación existe, solo se puede crear la oferta en una publicación existente. 
            self.saga.add_step("validar publicacion existente", self.validatePost(request,postId))
            # Solo es posible crear la oferta si la publicación no ha expirado.
            self.saga.add_step("validar publicacion, que no haya expirado", self.validatePostExpiration)
            # La oferta queda asociada al usuario de la sesión.
            self.saga.add_step("consultando el usuario en sesión", self.queryUserId(request.headers.get("Authorization")))
            # El usuario no debe poder ofertar en sus publicaciones.
            self.saga.add_step("validando que no se oferte sobre una publicación del mismo usuario", self.validateUserCreator())
            # obteniendo el costo de la maleta
            self.saga.add_step("obteniendo el costo de la maleta", self.queryRoute(request))
            # Se calcula la utilidad (score) de la oferta.
            self.saga.add_step("calculando el score de la oferta", self.createScore(request))

            #Crear la oferta
            self.saga.add_step("creando la oferta", self.createOffer(request),self.removeOffer)
            

            try:
                # En cualquier caso de error la información al finalizar debe ser consistente.
                self.saga.execute()
                self.logger.info("Saga completado exitosamente!")

                #obtener el user id
                user_id=self.global_context.get_data("userId")
                post=self.global_context.get_data("post")

                self.logger.info('armando la respuesta')
                current_utc = datetime.utcnow()
                return  {
                    "data": {
                        "id": self.global_context.get_data("offerCreated"),
                        "userId": user_id,
                        "createdAt": current_utc.isoformat(),
                        "postId": post.get_id()
                    },
                    "msg": f'Oferta creada con éxito, el score calculado es de {self.global_context.get_data("score_result")}'
                },HTTPStatus.CREATED
                

            except SagaError as e:
                self.logger.info(f"Error durante la ejecución del Saga: {str(e)}")
                return '', self.saga.getLastStatusCode()
        except Exception as e:
            self.logger.info(f"Error durante la ejecución de la Saga: {str(e)}")
            return '', self.saga.getLastStatusCode()
        



        