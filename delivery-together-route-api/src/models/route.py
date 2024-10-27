from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import validates
import re
from ..dataContext.sqlAlchemyContext import db
import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime


class Route(db.Model):
    __tablename__ = 'Route'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    flightId=db.Column(db.String())
    sourceAirportCode=db.Column(db.String())
    sourceCountry=db.Column(db.String())
    destinyAirportCode=db.Column(db.String())
    destinyCountry=db.Column(db.String())
    bagCost=db.Column(db.Integer)
    plannedStartDate = db.Column(DateTime, default=func.now())
    plannedEndDate = db.Column(DateTime, default=func.now())
    createdAt = db.Column(DateTime, default=func.now())
    updateAt = db.Column(DateTime, default=func.now())
    
   

    def __init__(self, flightId, sourceAirportCode, sourceCountry,destinyAirportCode,destinyCountry,bagCost,plannedStartDate,plannedEndDate):
        self.flightId=flightId
        self.sourceAirportCode=sourceAirportCode
        self.sourceCountry=sourceCountry
        self.destinyAirportCode=destinyAirportCode
        self.destinyCountry=destinyCountry
        self.bagCost=bagCost
        self.plannedStartDate=plannedStartDate
        self.plannedEndDate=plannedEndDate

    
class RouteSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Route
        include_relationships = True
        load_instance = True