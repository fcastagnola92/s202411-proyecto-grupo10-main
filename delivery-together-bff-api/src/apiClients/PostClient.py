from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
from  ..models.Post import Post
import logging
class PostClient:
    """
    Esta clase representa un cliente de la api de publicaciones
    Attributes:
        base_url (string): la url del servicio publicaciones
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
        self.logger.info(f'iniciando cliente de publicaciones')
        self.base_url = os.environ.get('POST_PATH')
        self.token=token

    def queryPost(self,idPost):
        """
        metodo para consumir la api de consulta de publicaciones
        Args:
            idPost (int): identificador de la publicación
        Return:
            Post (Post): objeto de la clase post
        """
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'la url de post {self.base_url}/posts/{idPost}')
            response = requests.get(f'{self.base_url}/posts/{idPost}', headers=headers)
            self.logger.info(f'consumiendo la consulta de post {idPost}')
            if response.status_code == 200:
                self.logger.info(f'status code 200 al consultar a post')
                data = response.json()
                if data:
                    self.logger.info(f'si hay datos en la respuesta {data}')
                    post=Post(data.get('id'),
                            data.get('routeId'),
                            data.get('userId'),
                            data.get('expireAt'),
                            data.get('createdAt'),
                            )
                    self.logger.info(f'convertido en el objeto post')
                    return post
                    
                else:
                    self.logger.info(f'el post {idPost} no fue encontrado')
                    return None
            else:
                self.logger.info(f"api de post responde con error: {response.status_code}, {response}, {response.data}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con post: {str(e)}")
            return None
        


    def queryMyPosts(self):
        """
        metodo para consumir la api de consulta de publicaciones
        Args:
            idPost (int): identificador de la publicación
        Return:
            Post (Post): objeto de la clase post
        """
        posts=[]
        try:
            headers = {
                'Authorization': self.token
            } 
            self.logger.info(f'la url de post {self.base_url}/posts?owner=me')
            response = requests.get(f'{self.base_url}//posts?owner=me', headers=headers)
            self.logger.info(f'consumiendo la consulta de post')
            if response.status_code == 200:
                self.logger.info(f'status code 200 al consultar a post')
                data = response.json()
                if data:
                    self.logger.info(f'si hay datos en la respuesta {data}')
                    posts.append(Post(data.get('id'),
                            data.get('routeId'),
                            data.get('userId'),
                            data.get('expireAt'),
                            data.get('createdAt'),
                            ))
                    self.logger.info(f'convertido en el objeto post')
                    return posts
                    
                else:
                    self.logger.info(f'no existen posts registrados')
                    return None
            else:
                self.logger.info(f"api de post responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con post: {str(e)}")
            return None
        

    def createPost(self,post):
        """
        metodo para consumir la api de creación de post
        Args:
            post (Post): post a crearse
        Return:
          new_post (Post)
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            data={
                "routeId": post.get_route(),
                "expireAt": post.get_expire()
            }
            response = requests.post(f'{self.base_url}/posts',json=data, headers=headers)
            print(f'{self.base_url}/posts   {data}')
            if response.status_code == 201:
                data = response.json()
                if data:
                    new_post=Post(id=data.get('id'),userId=data.get('userId'),createdAt=data.get('createdAt'),routeId=None,expireAt=None)
                    return new_post
                    
                else:
                    self.logger.info(f'error al crear el post')
                    return None
            else:
                self.logger.info(f"api de post responde con error: {response.status_code}, {response}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con post: {str(e)}")
            return None
        

    def removePost(self,postId):
        """
        metodo para consumir la api de eliminación de post
        Args:
            postId (uniqueidentifier): ruta a elminarse
        Return:
           na
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            } 
            
            response = requests.delete(f'{self.base_url}/posts/{postId}', headers=headers)
            if response.status_code == 200:
                return True
            else:
                self.logger.info(f"api de eliminar post responde con error: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error durante la comunicación con post: {str(e)}")
            return None

