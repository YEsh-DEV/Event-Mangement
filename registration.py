import random
from utils import PARTICIPANTS_FILE, load_json, save_json, validate_email, validate_phone
from events import get_event_by_title

def get_all_participants():
    """Returns all registered participants."""
    return load_json(PARTICIPANTS_FILE, [])

def save_participants(participants):
    """Saves participant list to JSON file."""
    return save_json(PARTICIPANTS_FILE, participants)

def get_event_enrollment_count(event_title):
    """
    Counts total participants registered for a given event.
    Demonstrates loop iteration and string matching.
    """
    participants = get_all_participants()
    count = 0
    for p in participants:
        if p["event"].strip().lower() == event_title.strip().lower():
            count += 1
    return count

def register_participant(name, age, gender, organization, phone, email, event_title):
    """
    Registers a new participant.
    Checks event capacity, validates inputs, and generates unique Reg ID.
    """
    if not name or not age or not gender or not organization or not phone or not email or not event_title:
        return False, "All registration fields are required."

    try:
        age_int = int(age)
        if age_int <= 0 or age_int > 120:
            return False, "Please enter a valid age between 1 and 120."
    except ValueError:
        return False, "Age must be a valid integer number."

    if not validate_email(email):
        return False, "Invalid email address format (e.g., user@example.com)."

    if not validate_phone(phone):
        return False, "Invalid phone number (must be at least 8 digits)."

    # Verify Event exists and has capacity
    event = get_event_by_title(event_title)
    if not event:
        return False, f"Selected event '{event_title}' does not exist."

    current_enrollment = get_event_enrollment_count(event_title)
    if current_enrollment >= event["capacity"]:
        return False, f"Event '{event_title}' is fully booked ({current_enrollment}/{event['capacity']} seats taken)."

    participants = get_all_participants()

    # Generate Unique Registration ID: REG-2026-XXXX
    seq_id = len(participants) + 1001
    reg_id = f"REG-2026-{seq_id}"

    fee = event["fee"]

    new_participant = {
        "reg_id": reg_id,
        "name": name.strip(),
        "age": age_int,
        "gender": gender.strip(),
        "organization": organization.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "event": event_title.strip(),
        "fee": fee,
        "amount_paid": 0.0,
        "payment_status": "Pending",
        "payment_mode": "N/A",
        "attendance": "Absent",
        "certificate_eligible": "Not Eligible"
    }

    participants.append(new_participant)
    if save_participants(participants):
        return True, f"Registration Successful!\nReg ID: {reg_id}\nFee: ${fee:.2f}"
    return False, "Failed to save registration."

def search_participants(search_term):
    """
    Searches participants by Name, Reg ID, Organization, or Event.
    Demonstrates list comprehensions and string matching.
    """
    participants = get_all_participants()
    if not search_term:
        return participants

    term = search_term.strip().lower()
    return [
        p for p in participants
        if term in p["name"].lower()
        or term in p["reg_id"].lower()
        or term in p["event"].lower()
        or term in p["organization"].lower()
    ]

def update_participant(reg_id, name, age, gender, organization, phone, email):
    """Updates participant details."""
    participants = get_all_participants()
    for i in range(len(participants)):
        if participants[i]["reg_id"] == reg_id:
            try:
                age_int = int(age)
            except ValueError:
                return False, "Invalid age value."

            participants[i]["name"] = name.strip()
            participants[i]["age"] = age_int
            participants[i]["gender"] = gender.strip()
            participants[i]["organization"] = organization.strip()
            participants[i]["phone"] = phone.strip()
            participants[i]["email"] = email.strip()

            save_participants(participants)
            return True, "Participant updated successfully."

    return False, "Participant not found."

def delete_participant(reg_id):
    """Deletes a participant by Reg ID."""
    participants = get_all_participants()
    for i in range(len(participants)):
        if participants[i]["reg_id"] == reg_id:
            del participants[i]
            save_participants(participants)
            return True, "Participant deleted successfully."

    return False, "Participant not found."
