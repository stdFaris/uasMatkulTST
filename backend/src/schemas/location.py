# src/schemas/location.py
from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    code: str

class Province(LocationBase):
    id: int
    
    class Config:
        from_attributes = True

class Regency(LocationBase):
    id: int
    province_id: int
    
    class Config:
        from_attributes = True

class District(LocationBase):
    id: int
    regency_id: int
    
    class Config:
        from_attributes = True

class Village(LocationBase):
    id: int
    district_id: int
    
    class Config:
        from_attributes = True