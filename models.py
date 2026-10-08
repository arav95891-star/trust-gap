from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Mechanic(Base):
    __tablename__ = "mechanics"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    password_hash = Column(String)
    garage_name = Column(String)
    tier = Column(String)

class Vehicle(Base):
    __tablename__ = "vehicles"
    reg_no = Column(String, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    
    rto_data = relationship("RTOData", back_populates="vehicle")
    insurance_data = relationship("InsuranceData", back_populates="vehicle")
    service_records = relationship("ServiceData", back_populates="vehicle")
    inspections = relationship("Inspection", back_populates="vehicle")

class RTOData(Base):
    __tablename__ = "rto_data"
    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, ForeignKey("vehicles.reg_no"))
    owner_serial = Column(Integer)
    challan_count = Column(Integer)
    fitness_valid_upto = Column(String)
    vehicle = relationship("Vehicle", back_populates="rto_data")

class InsuranceData(Base):
    __tablename__ = "insurance_data"
    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, ForeignKey("vehicles.reg_no"))
    policy_active = Column(Boolean)
    claim_history = Column(String)
    total_claim_amount = Column(Integer)
    vehicle = relationship("Vehicle", back_populates="insurance_data")

class ServiceData(Base):
    __tablename__ = "service_data"
    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, ForeignKey("vehicles.reg_no"))
    service_date = Column(String)
    mileage_km = Column(Integer)
    garage_name = Column(String)
    work_done = Column(String)
    vehicle = relationship("Vehicle", back_populates="service_records")

class Inspection(Base):
    __tablename__ = "inspections"
    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, ForeignKey("vehicles.reg_no"))
    
    engine_rating = Column(Integer)
    brakes_rating = Column(Integer)
    tyres_rating = Column(Integer)
    body_rating = Column(Integer)
    suspension_rating = Column(Integer)
    electricals_rating = Column(Integer)
    mechanic_notes = Column(String)
    
    # New mechanic tracking columns
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"))
    mechanic_name = Column(String)
    
    vehicle = relationship("Vehicle", back_populates="inspections")
    mechanic = relationship("Mechanic")