import os
import json
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
PARTICIPANTS_FILE = os.path.join(DATA_DIR, "participants.json")

def ensure_directories():
    """Ensures that data and reports directories exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def load_json(filepath, default_value=None):
    """
    Safely loads JSON data from a file.
    Demonstrates file handling and exception handling.
    """
    ensure_directories()
    if default_value is None:
        default_value = []
    
    if not os.path.exists(filepath):
        return default_value

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return default_value

def save_json(filepath, data):
    """
    Safely writes data to a JSON file.
    Demonstrates file operations and error handling.
    """
    ensure_directories()
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError:
        return False

def validate_email(email):
    """
    Validates email format using regular expressions.
    Checks for user pattern, domain, and TLD.
    """
    if not email:
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone):
    """
    Validates mobile phone number.
    Ensures input consists of numeric digits and meets length constraints.
    """
    if not phone:
        return False
    digits = phone.strip().replace(" ", "").replace("-", "")
    return digits.isdigit() and len(digits) >= 8

def init_sample_data():
    """
    Initializes sample events and participants if files are empty.
    Provides immediate testable data for demonstration.
    """
    ensure_directories()
    
    events = load_json(EVENTS_FILE, [])
    if not events:
        sample_events = [
            {
                "id": "EVT-101",
                "title": "Python Developer Summit 2026",
                "category": "Technology",
                "date": "2026-09-15",
                "time": "10:00 AM",
                "venue": "Main Auditorium",
                "capacity": 100,
                "fee": 500.0,
                "status": "Upcoming"
            },
            {
                "id": "EVT-102",
                "title": "AI & Data Science Workshop",
                "category": "Workshop",
                "date": "2026-09-20",
                "time": "02:00 PM",
                "venue": "Lab 302",
                "capacity": 30,
                "fee": 300.0,
                "status": "Upcoming"
            },
            {
                "id": "EVT-103",
                "title": "Annual Hackathon 2026",
                "category": "Competition",
                "date": "2026-10-05",
                "time": "09:00 AM",
                "venue": "Innovation Hall",
                "capacity": 60,
                "fee": 250.0,
                "status": "Upcoming"
            },
            {
                "id": "EVT-104",
                "title": "Cyber Security Seminar",
                "category": "Seminar",
                "date": "2026-10-12",
                "time": "11:30 AM",
                "venue": "Seminar Room B",
                "capacity": 45,
                "fee": 200.0,
                "status": "Upcoming"
            }
        ]
        save_json(EVENTS_FILE, sample_events)

    participants = load_json(PARTICIPANTS_FILE, [])
    if not participants:
        sample_participants = [
            {
                "reg_id": "REG-2026-1001",
                "name": "Alex Johnson",
                "age": 21,
                "gender": "Male",
                "organization": "Tech University",
                "phone": "9876543210",
                "email": "alex.j@email.com",
                "event": "Python Developer Summit 2026",
                "fee": 500.0,
                "amount_paid": 500.0,
                "payment_status": "Paid",
                "payment_mode": "UPI",
                "attendance": "Present",
                "certificate_eligible": "Eligible"
            },
            {
                "reg_id": "REG-2026-1002",
                "name": "Sophia Martinez",
                "age": 22,
                "gender": "Female",
                "organization": "City College",
                "phone": "9876543211",
                "email": "sophia.m@email.com",
                "event": "AI & Data Science Workshop",
                "fee": 300.0,
                "amount_paid": 150.0,
                "payment_status": "Partially Paid",
                "payment_mode": "Cash",
                "attendance": "Absent",
                "certificate_eligible": "Not Eligible"
            },
            {
                "reg_id": "REG-2026-1003",
                "name": "Rohan Sharma",
                "age": 20,
                "gender": "Male",
                "organization": "Global Institute",
                "phone": "9876543212",
                "email": "rohan.s@email.com",
                "event": "Python Developer Summit 2026",
                "fee": 500.0,
                "amount_paid": 0.0,
                "payment_status": "Pending",
                "payment_mode": "N/A",
                "attendance": "Absent",
                "certificate_eligible": "Not Eligible"
            },
            {
                "reg_id": "REG-2026-1004",
                "name": "Emily Chen",
                "age": 23,
                "gender": "Female",
                "organization": "Innovate Labs",
                "phone": "9876543213",
                "email": "emily.c@email.com",
                "event": "Annual Hackathon 2026",
                "fee": 250.0,
                "amount_paid": 250.0,
                "payment_status": "Paid",
                "payment_mode": "Credit Card",
                "attendance": "Present",
                "certificate_eligible": "Eligible"
            }
        ]
        save_json(PARTICIPANTS_FILE, sample_participants)
