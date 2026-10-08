from pydantic import BaseModel
from typing import List, Optional

class RTODataSchema(BaseModel):
    owner_serial: int
    challan_count: int
    fitness_valid_upto: str
    model_config = {"from_attributes": True}

class InsuranceDataSchema(BaseModel):
    policy_active: bool
    claim_history: str
    total_claim_amount: int
    model_config = {"from_attributes": True}

class ServiceDataSchema(BaseModel):
    service_date: str
    mileage_km: int
    garage_name: str
    work_done: str
    model_config = {"from_attributes": True}

class InspectionCreate(BaseModel):
    reg_no: str
    engine_rating: int
    brakes_rating: int
    tyres_rating: int
    body_rating: int
    suspension_rating: int
    electricals_rating: int
    mechanic_notes: str

class InspectionSchema(InspectionCreate):
    id: int
    mechanic_name: Optional[str] = None
    model_config = {"from_attributes": True}

# --- LOGIN SCHEMAS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    mechanic_name: str

class VehicleReportResponse(BaseModel):
    reg_no: str
    make: str
    model: str
    year: int
    
    rto_data: List[RTODataSchema] = []
    insurance_data: List[InsuranceDataSchema] = []
    service_records: List[ServiceDataSchema] = []
    inspections: List[InspectionSchema] = []
    
    condition_score: int
    estimated_repair_cost: str
    odometer_rollback_detected: bool
    
    # New field to show the mechanic on the report
    inspected_by: Optional[str] = None

    model_config = {"from_attributes": True}