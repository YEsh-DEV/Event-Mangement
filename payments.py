from registration import get_all_participants, save_participants

def record_payment(reg_id, additional_amount, payment_mode):
    """
    Records payment for a participant.
    Updates amount_paid, payment_status, payment_mode, and certificate eligibility.
    Demonstrates numerical logic, conditional updating, and data persistence.
    """
    if not reg_id:
        return False, "Registration ID is required."

    try:
        payment_amt = float(additional_amount)
        if payment_amt <= 0:
            return False, "Payment amount must be greater than zero."
    except ValueError:
        return False, "Please enter a valid numeric payment amount."

    if not payment_mode or payment_mode == "Select Mode":
        return False, "Please select a valid payment mode (UPI, Cash, Credit/Debit Card)."

    participants = get_all_participants()
    for p in participants:
        if p["reg_id"] == reg_id:
            current_paid = p.get("amount_paid", 0.0)
            fee = p.get("fee", 0.0)
            new_total_paid = current_paid + payment_amt

            if new_total_paid > fee:
                return False, f"Payment exceeds fee! Outstanding due is only ${fee - current_paid:.2f}."

            p["amount_paid"] = round(new_total_paid, 2)
            p["payment_mode"] = payment_mode

            # Update Payment Status
            if p["amount_paid"] >= fee:
                p["payment_status"] = "Paid"
            elif p["amount_paid"] > 0:
                p["payment_status"] = "Partially Paid"
            else:
                p["payment_status"] = "Pending"

            # Auto-update certificate eligibility
            if p["payment_status"] == "Paid" and p.get("attendance") == "Present":
                p["certificate_eligible"] = "Eligible"
            else:
                p["certificate_eligible"] = "Not Eligible"

            save_participants(participants)
            due_amount = fee - p["amount_paid"]
            return True, f"Payment recorded successfully!\nStatus: {p['payment_status']}\nRemaining Due: ${due_amount:.2f}"

    return False, "Participant with given Registration ID was not found."

def get_payment_summary():
    """
    Calculates overall payment statistics.
    Demonstrates loops, dict operations, and numerical aggregation.
    """
    participants = get_all_participants()
    total_fee_expected = sum(p["fee"] for p in participants)
    total_collected = sum(p["amount_paid"] for p in participants)
    outstanding_dues = total_fee_expected - total_collected

    paid_count = sum(1 for p in participants if p["payment_status"] == "Paid")
    partial_count = sum(1 for p in participants if p["payment_status"] == "Partially Paid")
    pending_count = sum(1 for p in participants if p["payment_status"] == "Pending")

    collection_rate = (total_collected / total_fee_expected * 100) if total_fee_expected > 0 else 0.0

    return {
        "total_fee_expected": total_fee_expected,
        "total_collected": total_collected,
        "outstanding_dues": outstanding_dues,
        "paid_count": paid_count,
        "partial_count": partial_count,
        "pending_count": pending_count,
        "collection_rate": collection_rate
    }

def get_pending_dues_list():
    """Returns all participants with unpaid dues."""
    participants = get_all_participants()
    return [p for p in participants if p["fee"] - p["amount_paid"] > 0]
