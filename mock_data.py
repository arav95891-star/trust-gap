import hashlib
from database import engine, SessionLocal, Base
from models import Vehicle, RTOData, InsuranceData, ServiceData, Inspection, Mechanic

def get_password_hash(password: str, salt: str) -> str:
    """Hashes the password with SHA-256, using the username as the salt."""
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def seed_database():
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # --- SEED MECHANICS ---
    mechanics = [
        Mechanic(username="mech1", full_name="Rahul Sharma", password_hash=get_password_hash("demo123", "mech1"), garage_name="Sharma Auto (Authorized)", tier="Tier 1"),
        Mechanic(username="mech2", full_name="Vikram Singh", password_hash=get_password_hash("demo123", "mech2"), garage_name="Vikram Motors", tier="Tier 2"),
        Mechanic(username="mech3", full_name="Amit Patel", password_hash=get_password_hash("demo123", "mech3"), garage_name="Patel Garage", tier="Tier 2")
    ]
    db.add_all(mechanics)

    # --- CREATE 8 VEHICLES ---
    vehicles = [
        Vehicle(reg_no="DL01AB1234", make="Maruti Suzuki", model="Swift", year=2020),
        Vehicle(reg_no="MH02XY5678", make="Hyundai", model="i20", year=2019),
        Vehicle(reg_no="KA03QW9876", make="Honda", model="City", year=2021),
        Vehicle(reg_no="UP14DZ1122", make="Tata", model="Nexon", year=2018),
        Vehicle(reg_no="TN05BM4455", make="Toyota", model="Innova", year=2017),
        Vehicle(reg_no="GJ06JK9988", make="Kia", model="Seltos", year=2022),
        Vehicle(reg_no="WB07KL3344", make="Mahindra", model="Thar", year=2021),
        Vehicle(reg_no="RJ14CQ7777", make="Ford", model="EcoSport", year=2019)
    ]
    db.add_all(vehicles)

    rto_records = [
        RTOData(reg_no="DL01AB1234", owner_serial=1, challan_count=0, fitness_valid_upto="2035-01-10"),
        RTOData(reg_no="MH02XY5678", owner_serial=2, challan_count=2, fitness_valid_upto="2034-05-12"),
        RTOData(reg_no="KA03QW9876", owner_serial=1, challan_count=1, fitness_valid_upto="2036-08-20"),
        RTOData(reg_no="UP14DZ1122", owner_serial=3, challan_count=5, fitness_valid_upto="2033-11-05"),
        RTOData(reg_no="TN05BM4455", owner_serial=1, challan_count=0, fitness_valid_upto="2032-02-14"),
        RTOData(reg_no="GJ06JK9988", owner_serial=1, challan_count=0, fitness_valid_upto="2037-09-30"),
        RTOData(reg_no="WB07KL3344", owner_serial=2, challan_count=3, fitness_valid_upto="2036-12-01"),
        RTOData(reg_no="RJ14CQ7777", owner_serial=1, challan_count=1, fitness_valid_upto="2034-07-22")
    ]
    db.add_all(rto_records)

    insurance_records = [
        InsuranceData(reg_no="DL01AB1234", policy_active=True, claim_history="Clean", total_claim_amount=0),
        InsuranceData(reg_no="MH02XY5678", policy_active=True, claim_history="Clean", total_claim_amount=0),
        InsuranceData(reg_no="KA03QW9876", policy_active=True, claim_history="Major Frontal Collision", total_claim_amount=150000),
        InsuranceData(reg_no="UP14DZ1122", policy_active=False, claim_history="Clean", total_claim_amount=0),
        InsuranceData(reg_no="TN05BM4455", policy_active=True, claim_history="Clean", total_claim_amount=0),
        InsuranceData(reg_no="GJ06JK9988", policy_active=True, claim_history="Clean", total_claim_amount=0),
        InsuranceData(reg_no="WB07KL3344", policy_active=True, claim_history="Minor Scrape", total_claim_amount=5000),
        InsuranceData(reg_no="RJ14CQ7777", policy_active=True, claim_history="Clean", total_claim_amount=0)
    ]
    db.add_all(insurance_records)

    service_records = [
        ServiceData(reg_no="DL01AB1234", service_date="2021-06-01", mileage_km=10000, garage_name="Maruti Auth", work_done="Oil Change"),
        ServiceData(reg_no="DL01AB1234", service_date="2022-06-01", mileage_km=22000, garage_name="Maruti Auth", work_done="General Service"),
        ServiceData(reg_no="KA03QW9876", service_date="2022-03-15", mileage_km=15000, garage_name="Honda Auth", work_done="Bumper & Radiator Replace"),
        ServiceData(reg_no="UP14DZ1122", service_date="2020-01-10", mileage_km=45000, garage_name="Local Garage", work_done="Brakes"),
        ServiceData(reg_no="UP14DZ1122", service_date="2021-02-15", mileage_km=62000, garage_name="Local Garage", work_done="Suspension"),
        ServiceData(reg_no="UP14DZ1122", service_date="2023-08-20", mileage_km=31000, garage_name="Shady Motors", work_done="General Service"), 
        ServiceData(reg_no="TN05BM4455", service_date="2020-10-10", mileage_km=50000, garage_name="Toyota Auth", work_done="Clutch replace"),
        ServiceData(reg_no="GJ06JK9988", service_date="2023-01-01", mileage_km=12000, garage_name="Kia Auth", work_done="Oil Change"),
        ServiceData(reg_no="WB07KL3344", service_date="2022-05-10", mileage_km=28000, garage_name="Mahindra Auth", work_done="4x4 check"),
        ServiceData(reg_no="RJ14CQ7777", service_date="2021-12-12", mileage_km=35000, garage_name="Ford Auth", work_done="Battery replace")
    ]
    db.add_all(service_records)

    db.commit()
    db.close()
    print("Mock data and 3 Mechanics successfully loaded into trust_gap.db!")

if __name__ == "__main__":
    seed_database()