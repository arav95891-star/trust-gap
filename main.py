from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import io
import hashlib
import secrets
from reportlab.pdfgen import canvas

from database import engine, SessionLocal, Base
import models
import schemas
import scoring

# ─── STARTUP: create tables, then seed if database is empty ───────────────────
Base.metadata.create_all(bind=engine)

def _seed_if_empty():
    db = SessionLocal()
    try:
        count = db.query(models.Vehicle).count()
        if count == 0:
            print("Database is empty — seeding mock data automatically...")
            # Import here to avoid circular-import issues at module level
            from mock_data import seed_database
            seed_database()
            print("Seeding complete.")
        else:
            print(f"Database already has {count} vehicle(s). Skipping seed.")
    finally:
        db.close()

_seed_if_empty()
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(title="The Trust Gap - Vehicle Trust API")
templates = Jinja2Templates(directory="templates")

# Simple in-memory token store
active_tokens = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


# ─── PUBLIC ENDPOINTS ─────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/vehicle/{reg_no}")
def get_vehicle(reg_no: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.reg_no == reg_no).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.get("/report/{reg_no}", response_model=schemas.VehicleReportResponse)
def get_full_report(reg_no: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.reg_no == reg_no).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    rollback = scoring.detect_odometer_rollback(vehicle.service_records)
    score = scoring.calculate_condition_score(vehicle.inspections)
    cost = scoring.forecast_repair_cost(score, vehicle.insurance_data)

    inspected_by = None
    if vehicle.inspections:
        latest = vehicle.inspections[-1]
        mechanic = db.query(models.Mechanic).filter(
            models.Mechanic.id == latest.mechanic_id
        ).first()
        if mechanic:
            inspected_by = f"{latest.mechanic_name} ({mechanic.garage_name})"

    return schemas.VehicleReportResponse(
        reg_no=vehicle.reg_no,
        make=vehicle.make,
        model=vehicle.model,
        year=vehicle.year,
        rto_data=vehicle.rto_data,
        insurance_data=vehicle.insurance_data,
        service_records=vehicle.service_records,
        inspections=vehicle.inspections,
        condition_score=score,
        estimated_repair_cost=cost,
        odometer_rollback_detected=rollback,
        inspected_by=inspected_by,
    )


@app.get("/report/{reg_no}/pdf")
def get_report_pdf(reg_no: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.reg_no == reg_no).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    rollback = scoring.detect_odometer_rollback(vehicle.service_records)
    score = scoring.calculate_condition_score(vehicle.inspections)
    cost = scoring.forecast_repair_cost(score, vehicle.insurance_data)

    inspected_by_text = "Pending Physical Inspection"
    if vehicle.inspections:
        latest = vehicle.inspections[-1]
        mechanic = db.query(models.Mechanic).filter(
            models.Mechanic.id == latest.mechanic_id
        ).first()
        if mechanic:
            inspected_by_text = f"{latest.mechanic_name} ({mechanic.garage_name})"

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, "The Trust Gap - Verified Vehicle Passport")

    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Registration No: {vehicle.reg_no}")
    p.drawString(50, 750, f"Vehicle: {vehicle.year} {vehicle.make} {vehicle.model}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 710, "Trust & Scoring Metrics")
    p.setFont("Helvetica", 12)
    p.drawString(50, 690, f"Condition Score: {score}/100")
    p.drawString(50, 670, f"Inspected by: {inspected_by_text}")

    rollback_text = "WARNING: DETECTED" if rollback else "Clear"
    p.drawString(50, 650, f"Odometer Rollback: {rollback_text}")
    p.drawString(50, 630, f"12-24 Month Cost Forecast: {cost}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=trust_report_{reg_no}.pdf"
        },
    )


# ─── AUTH ENDPOINTS ───────────────────────────────────────────────────────────

@app.post("/login", response_model=schemas.LoginResponse)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    mechanic = db.query(models.Mechanic).filter(
        models.Mechanic.username == req.username
    ).first()

    if not mechanic or mechanic.password_hash != get_password_hash(
        req.password, req.username
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = secrets.token_hex(16)
    active_tokens[token] = {
        "id": mechanic.id,
        "name": mechanic.full_name,
        "garage": mechanic.garage_name,
    }

    return schemas.LoginResponse(token=token, mechanic_name=mechanic.full_name)


@app.post("/logout")
def logout(authorization: str = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        active_tokens.pop(token, None)
    return {"message": "Logged out successfully"}


# ─── PROTECTED ENDPOINT ───────────────────────────────────────────────────────

@app.post("/inspection", response_model=schemas.InspectionSchema)
def create_inspection(
    inspection: schemas.InspectionCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.split(" ")[1]
    if token not in active_tokens:
        raise HTTPException(
            status_code=401, detail="Session expired. Please log in again."
        )

    mech_data = active_tokens[token]

    db_inspection = models.Inspection(
        **inspection.dict(),
        mechanic_id=mech_data["id"],
        mechanic_name=mech_data["name"],
    )
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection