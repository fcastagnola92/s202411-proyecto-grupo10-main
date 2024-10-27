class VerificationCard:
    """
    Esta clase representa un solicitud de verificación de trajeta
    Attributes:
        card_number (string): numero de tarjeta 
        cvv (string): cvv de tarjeta 
        expiration_date (string): fecha de expiración de la  tarjeta YY/MM
        card_holder_name (string): titular 
        transaction_identifier (string): identificador de la trasaccion de verificación
    """


    def __init__(self,card_number, cvv, expiration_date, card_holder_name, transaction_identifier):
        self.card_number=card_number
        self.cvv=cvv
        self.expiration_date=expiration_date
        self.card_holder_name=card_holder_name
        self.transaction_identifier=transaction_identifier


    def get_card_number(self):
        return self.card_number
    
    def get_cvv(self):
        return self.cvv
    
    def get_expiration_date(self):
        return self.expiration_date
    
    def get_card_holder_name(self):
        return self.card_holder_name
    
    def get_transaction_identifier(self):
        return self.transaction_identifier

    