import json
import os

CLINIC_OPEN = 9  # 9:00 AM
CLINIC_CLOSE = 17 # 5:00 PM
AVAILABLE_SLOTS = ["09:30 AM", "11:00 AM", "02:00 PM", "04:00 PM"]

RULES_FILE = "dynamic_rules.json"
BOOKED_APPOINTMENTS = []

def get_dynamic_rules():
    if not os.path.exists(RULES_FILE):
        return []
    with open(RULES_FILE, "r") as f:
        return json.load(f)

def save_dynamic_rule(new_rule: str):
    rules = get_dynamic_rules()
    if new_rule not in rules:
        rules.append(new_rule)
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=2)

def clear_rules():
    global BOOKED_APPOINTMENTS
    BOOKED_APPOINTMENTS = []
    if os.path.exists(RULES_FILE):
        os.remove(RULES_FILE)

def attempt_booking(time_str: str) -> dict:
    """Deterministic Database State Machine validating constraints."""
    try:
        # Simple extraction logic for parsing hours (e.g. "8:00 AM" -> 8)
        clean_time = time_str.upper().strip()
        parts = clean_time.split(":")
        hour = int(parts[0])
        if "PM" in clean_time and hour != 12:
            hour += 12
        if "AM" in clean_time and hour == 12:
            hour = 0
            
        if hour < CLINIC_OPEN or hour >= CLINIC_CLOSE:
            return {"success": False, "code": "ERR_OUT_OF_BOUNDS", "error": f"Time slot {time_str} is outside operating hours (9 AM - 5 PM)."}
        
        # Match standard slots standard format
        standardized_slots = [s.upper().strip() for s in AVAILABLE_SLOTS]
        if clean_time not in standardized_slots and f"0{clean_time}" not in standardized_slots:
            return {"success": False, "code": "ERR_SLOT_UNAVAILABLE", "error": f"Time slot {time_str} is not an open available slot today."}
            
        BOOKED_APPOINTMENTS.append(time_str)
        return {"success": True, "code": "SUCCESS_BOOKED", "message": f"Successfully confirmed appointment for {time_str}."}
    except Exception:
        return {"success": False, "code": "ERR_INVALID_FORMAT", "error": "Invalid time format provided to database."}
