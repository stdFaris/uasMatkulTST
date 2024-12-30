from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from ..config.database import Base

class TimeStampedModel:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)