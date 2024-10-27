class Offer:
    """
    Esta clase representa una oferta
    Attributes:
        id (uniqueidentifier) id de la oferta
        postId (uniqueidentifier): id de la publicacion
        description (string): descripcion 
        size (string): tamaño
        fragile (bool): delicado
        offer (int): valor ofertado
        createdAt (date): fecha de creación
        userId: (uniqueidentifier): identificador del usuairo que la creó
        score (int):  la utilidad  con la oferta
    """
    def __init__(self,postId,description, size, fragile, offer, id=None, createdAt=None, userId=None):
        self.postId=postId
        self.description=description
        self.size=size
        self.fragile=fragile
        self.offer=offer
        self.id=id
        self.createdAt=createdAt
        self.userId=userId
        self.score=0

    def get_post_id(self):
        return self.postId
    
    def get_description(self):
        return self.description
    
    def get_size(self):
        return self.size
    
    def get_fragile(self):
        return self.fragile
    
    def get_offer(self):
        return self.offer
    
    def get_id(self):
        return self.id
    
    def get_createdAt(self):
        return self.createdAt
    
    def get_userId(self):
        return self.userId
    
    def get_score(self):
        return self.score
    
    def set_score(self,score):
        self.score=score
    
    def to_dict(self):
        return {'id': self.id,'userId':self.userId, 'description': self.description, 'size': self.size,'fragile':self.fragile, 'offer':self.offer,'score':self.score,'createdAt':self.createdAt}
    