class User:
    """
    Esta clase representa un usuario consultado
    Attributes:
        id (string): id del usuario
        email (string): email del usuario 
    """

    def __init__(self,id, email):
        self.id=id
        self.email=email


    def get_id(self):
        return self.id
    
    def get_email(self):
        return self.email
    