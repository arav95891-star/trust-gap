def detect_odometer_rollback(service_records) -> bool:
    """
    Checks if a car's mileage ever goes backwards over time.
    Returns True if a rollback is detected, False otherwise.
    """
    # First, we sort the records by date (oldest first)
    # This is like using std::sort in C++ with a custom comparator
    sorted_records = sorted(service_records, key=lambda record: record.service_date)
    
    highest_mileage_so_far = 0
    
    for record in sorted_records:
        if record.mileage_km < highest_mileage_so_far:
            # The mileage dropped! This is physical proof of tampering.
            return True 
            
        if record.mileage_km > highest_mileage_so_far:
            # Update our tracker to the new highest mileage
            highest_mileage_so_far = record.mileage_km
            
    return False

def calculate_condition_score(inspections) -> int:
    """
    Takes mechanic ratings (1-5) and converts them into a score out of 100.
    """
    # If the mechanic hasn't inspected the car yet, return 0
    if not inspections:
        return 0 

    # We grab the most recent inspection (the last one in the list)
    latest = inspections[-1]
    
    # 6 categories, max rating of 5. Total possible points = 30.
    total_points = (
        latest.engine_rating + 
        latest.brakes_rating + 
        latest.tyres_rating + 
        latest.body_rating + 
        latest.suspension_rating + 
        latest.electricals_rating
    )
    
    # Calculate percentage (Score / 30) * 100, and convert to an integer
    score = int((total_points / 30.0) * 100)
    
    return score

def forecast_repair_cost(condition_score: int, insurance_records) -> str:
    """
    A rule-based engine that predicts repair costs for the next 12-24 months.
    """
    # If no inspection has happened, we can't forecast
    if condition_score == 0:
        return "Cannot forecast: Pending Physical Inspection"
        
    # Rule 1: Determine base cost using the Condition Score
    if condition_score >= 80:
        forecast = "₹5,000 - ₹12,000 (Routine Maintenance expected)"
    elif condition_score >= 50:
        forecast = "₹15,000 - ₹35,000 (Moderate wear: likely brakes, tyres, or suspension)"
    else:
        forecast = "₹45,000+ (High risk: Major engine or structural work likely)"

    # Rule 2: Check for major accident history
    # Even if the car looks fine now, a bad crash means hidden issues might pop up
    for record in insurance_records:
        if record.total_claim_amount > 50000:
            forecast += " | *WARNING: Past major accident increases future complication risk*"
            break # We only need to find one major accident to trigger the warning

    return forecast