class Aggregation_Exception(Exception):
    def __init__(self, mensaje="Ha ocurrido un error personalizado", status_code=500):
        self.mensaje = mensaje
        self.status_code = status_code
        super().__init__(self.mensaje)