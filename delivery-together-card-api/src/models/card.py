from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import validates
import re
from ..dataContext.sqlAlchemyContext import db
import uuid
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime,Enum

import enum




class Issuer(enum.Enum):
    VISA='VISA'
    MASTERCARD='MASTERCARD'
    AMERICAN_EXPRESS='AMERICAN_EXPRESS'
    DISCOVER='DISCOVER'
    DINERS_CLUB='DINERS_CLUB'
    UNKNOWN='UNKNOWN'

class Status(enum.Enum):
    POR_VERIFICAR='POR_VERIFICAR'
    RECHAZADA='RECHAZADA'
    APROBADA='APROBADA'

class Card(db.Model):
    __tablename__ = 'Card'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    token=db.Column(db.String(256))
    userId=db.Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    lastFourDigits=db.Column(db.String(4))
    ruv=db.Column(db.String())
    issuer=db.Column(Enum(Issuer))
    status=db.Column(Enum(Status))
    createdAt = db.Column(DateTime, default=func.now())
    updateAt = db.Column(DateTime, default=func.now())
    userEmail=db.Column(db.String(256))

   

    def __init__(self,id,token, userId,lastFourDigits,ruv,issuer,userEmail):
        self.id=id
        self.token=token
        self.userId=userId
        self.lastFourDigits=lastFourDigits
        self.ruv=ruv
        self.issuer=issuer
        self.status=Status.POR_VERIFICAR
        self.userEmail=userEmail

    def set_status(self,status):
        self.status=status

    def set_updateDate(self,new_date):
        self.updateAt=new_date

    def to_dict(self):
        return {
            'id': str(self.id),
            'token': self.token,
            'userId': str(self.userId),
            'lastFourDigits': self.lastFourDigits,
            'ruv': self.ruv,
            'createdAt': self.createdAt.isoformat(),
            'updateAt': self.updateAt.isoformat()
        }

       

    
class CardSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Card
        include_relationships = True
        load_instance = True