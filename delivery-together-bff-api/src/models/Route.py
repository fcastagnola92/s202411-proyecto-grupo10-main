class Route:
    """
    Esta clase representa una ruta
    Attributes:
        id (uniqueidentifier) identificador de la ruta
        flightId (str) id de vuelo
        sourceAirportCode (str) codigo aerepuerto origen
        sourceCountry (str) pais origen
        destinyAirportCode (str) codigo aerepuerto destino
        destinyCountry (str) pais destino
        bagCost (int) costo de la maleta
        plannedStartDate (date) fecha de inicio de la ruta
        plannedEndDate (date) fecha fin de la ruta
    """
    def __init__(self,id,flightId,sourceAirportCode,sourceCountry,destinyAirportCode,destinyCountry,bagCost,plannedStartDate,plannedEndDate):
        self.id=id
        self.flightId=flightId
        self.sourceAirportCode=sourceAirportCode
        self.sourceCountry=sourceCountry
        self.destinyAirportCode=destinyAirportCode
        self.destinyCountry=destinyCountry
        self.bagCost=bagCost
        self.plannedStartDate=plannedStartDate
        self.plannedEndDate=plannedEndDate


    def get_id(self):
        return self.id

    def get_flight_id(self):
        return self.flightId

    def get_source_airport_code(self):
        return self.sourceAirportCode

    def get_source_country(self):
        return self.sourceCountry

    def get_destiny_airport_code(self):
        return self.destinyAirportCode

    def get_destiny_country(self):
        return self.destinyCountry

    def get_bag_cost(self):
        return self.bagCost

    def get_planned_start_date(self):
        return self.plannedStartDate

    def get_planned_end_date(self):
        return self.plannedEndDate

    def set_id(self, new_id):
        self.id = new_id

    def set_flight_id(self, new_flight_id):
        self.flightId = new_flight_id

    def set_source_airport_code(self, new_source_airport_code):
        self.sourceAirportCode = new_source_airport_code

    def set_source_country(self, new_source_country):
        self.sourceCountry = new_source_country

    def set_destiny_airport_code(self, new_destiny_airport_code):
        self.destinyAirportCode = new_destiny_airport_code

    def set_destiny_country(self, new_destiny_country):
        self.destinyCountry = new_destiny_country

    def set_bag_cost(self, new_bag_cost):
        self.bagCost = new_bag_cost

    def set_planned_start_date(self, new_planned_start_date):
        self.plannedStartDate = new_planned_start_date

    def set_planned_end_date(self, new_planned_end_date):
        self.plannedEndDate = new_planned_end_date

