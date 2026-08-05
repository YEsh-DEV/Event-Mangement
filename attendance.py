from registration import get_all_participants, save_participants

def mark_attendance(reg_id, status):
    """
    Marks attendance status ('Present' or 'Absent') and evaluates certificate eligibility.
    Certificate Eligibility Condition: Present status AND Paid status.
    """
    if status not in ["Present", "Absent"]:
        return False, "Invalid attendance status."

    participants = get_all_participants()
    for p in participants:
        if p["reg_id"] == reg_id:
            p["attendance"] = status

            # Check certificate eligibility rule
            if p["attendance"] == "Present" and p.get("payment_status") == "Paid":
                p["certificate_eligible"] = "Eligible"
            else:
                p["certificate_eligible"] = "Not Eligible"

            save_participants(participants)
            return True, f"Attendance marked as '{status}' for {p['name']} ({reg_id}). Certificate Status: {p['certificate_eligible']}."

    return False, "Participant not found."

def get_attendance_summary(event_title=None):
    """
    Generates attendance and certificate statistics for all events or a specific event.
    Demonstrates filtering, loops, and percentage calculations.
    """
    participants = get_all_participants()
    if event_title:
        participants = [p for p in participants if p["event"].strip().lower() == event_title.strip().lower()]

    total = len(participants)
    present_count = sum(1 for p in participants if p.get("attendance") == "Present")
    absent_count = sum(1 for p in participants if p.get("attendance") == "Absent")
    eligible_count = sum(1 for p in participants if p.get("certificate_eligible") == "Eligible")

    attendance_rate = (present_count / total * 100) if total > 0 else 0.0

    return {
        "total": total,
        "present": present_count,
        "absent": absent_count,
        "eligible_certificates": eligible_count,
        "attendance_rate": attendance_rate
    }
