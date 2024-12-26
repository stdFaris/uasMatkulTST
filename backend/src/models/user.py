from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    ADMIN = "admin"

class ServiceType(str, enum.Enum):
    HOUSEMAID = "pembantu"
    GARDENER = "ahli_kebun"
    MASSEUR = "ahli_pijat"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole))
    
    # Relationships
    customer_profile = relationship("CustomerProfile", back_populates="user", uselist=False)
    partner_profile = relationship("PartnerProfile", back_populates="user", uselist=False)

class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(Float, default=0.0)
    location = Column(String)
    
    user = relationship("User", back_populates="customer_profile")

class PartnerProfile(Base):
    __tablename__ = "partner_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float, default=0.0)
    location = Column(String)
    service_type = Column(Enum(ServiceType))
    hourly_rate = Column(Float)
    working_hours_start = Column(String)  # Format: "HH:MM"
    working_hours_end = Column(String)    # Format: "HH:MM"
    
    user = relationship("User", back_populates="partner_profile")