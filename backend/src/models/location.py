from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Province(BaseModel):
    __tablename__ = "provinces"
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    
    regencies = relationship("Regency", back_populates="province")

class Regency(BaseModel):
    __tablename__ = "regencies"
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    
    province = relationship("Province", back_populates="regencies")
    districts = relationship("District", back_populates="regency")

class District(BaseModel):
    __tablename__ = "districts"
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    regency_id = Column(Integer, ForeignKey("regencies.id"))
    
    regency = relationship("Regency", back_populates="districts")
    villages = relationship("Village", back_populates="district")

class Village(BaseModel):
    __tablename__ = "villages"
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    
    district = relationship("District", back_populates="villages")