class VerificationCardResponse:
    """
    Esta clase representa un respuesta de verificación de tarjeta
    Attributes:
        ruv (string): registro único de verificación,
        createdAt (date): fecha de creación de la solicitud
        issuer (string): *Nombre del emisor de la tarjeta,
        task_status (string): estado 
        token (string): Token de la tarjeta de crédito,
        transactionIdentifier (string): Valor único definido por el cliente
    """


    def __init__(self,ruv, createdAt,issuer,task_status,token,transactionIdentifier):
        self.ruv=ruv
        self.createdAt=createdAt
        self.issuer=issuer
        self.task_status=task_status
        self.token=token
        self.transactionIdentifier=transactionIdentifier


    def get_ruv(self):
        return self.ruv

    def get_createdAt(self):
        return self.createdAt

    def get_issuer(self):
        return self.issuer

    def get_task_status(self):
        return self.task_status

    def get_token(self):
        return self.token

    def get_transactionIdentifier(self):
        return self.transactionIdentifier

    