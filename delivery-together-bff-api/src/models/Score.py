class Score:
    """
    Esta clase representa un Score o utilidad
    Attributes:
        bagCost (int): costo
        offer (int): oferta
        offerId (uniqueidentifier): id de la oferta
        routeId (uniqueidentifier): id de la ruta
        size (string): tamaño
    """
    def __init__(self,bagCost,offer, offerId, routeId, size):
        self.bagCost=bagCost
        self.offer=offer
        self.offerId=offerId
        self.routeId=routeId
        self.size=size

    def get_bag_cost(self):
        return self.bagCost
    
    def get_offer(self):
        return self.offer
    
    def get_offer_id(self):
        return self.offerId
    
    def get_route_id(self):
        return self.routeId
    
    def get_size(self):
        return self.size