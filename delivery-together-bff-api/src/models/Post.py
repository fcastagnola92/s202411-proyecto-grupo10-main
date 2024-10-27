class Post:
    """
    Esta clase representa una publicación
    Attributes:
        id (uniqueidentifier): id de la publicacion
        routeId (uniqueidentifier): id de la ruta de la publicacion
        userId (uniqueidentifier): el user id de la publicación
        expireAt (date): fecha de expiración
        createdAt (date): fecha de creación
    """
    def __init__(self,id,routeId,userId,expireAt, createdAt):
        self.id=id
        self.routeId=routeId
        self.userId=userId
        self.expireAt=expireAt
        self.createdAt=createdAt

    def get_id(self):
        return self.id
    
    def get_route(self):
        return self.routeId
    
    def get_user(self):
        return self.userId
    
    def get_expire(self):
        return self.expireAt
    
    def get_createdAt(self):
        return self.createdAt