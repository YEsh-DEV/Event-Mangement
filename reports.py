import os
import csv
from datetime import datetime
from utils import REPORTS_DIR, ensure_directories
from events import get_all_events
from registration import get_all_participants
from analytics import generate_full_analytics

def generate_text_report():
    """
    Generates a timestamped plain-text report.
    Demonstrates string formatting, file output operations, and timestamping.
    """
    ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"event_report_{timestamp}.txt"
    filepath = os.path.join(REPORTS_DIR, filename)

    events = get_all_events()
    participants = get_all_participants()
    analytics = generate_full_analytics()

    lines = []
    lines.append("=" * 70)
    lines.append("                 EVENT MANAGEMENT SYSTEM REPORT")
    lines.append(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")

    lines.append("--- 1. OVERALL EXECUTIVE SUMMARY ---")
    lines.append(f"Total Events:            {analytics['total_events']}")
    lines.append(f"Total Participants:      {analytics['total_participants']}")
    lines.append(f"Capacity Occupancy Rate: {analytics['occupancy_rate']:.2f}%")
    lines.append(f"Total Fees Expected:     ${analytics['total_fee_expected']:.2f}")
    lines.append(f"Total Revenue Collected: ${analytics['total_revenue_collected']:.2f}")
    lines.append(f"Outstanding Dues:        ${analytics['outstanding_dues']:.2f}")
    lines.append(f"Collection Rate:         {analytics['collection_rate']:.2f}%")
    lines.append(f"Most Popular Event:      {analytics['most_popular_event']} ({analytics['most_popular_count']} participants)")
    lines.append(f"Top Revenue Event:       {analytics['top_revenue_event']} (${analytics['top_revenue_amount']:.2f})")
    lines.append("")

    lines.append("--- 2. EVENTS LIST ---")
    lines.append(f"{'ID':<10} {'Title':<30} {'Category':<15} {'Capacity':<10} {'Fee ($)':<8}")
    lines.append("-" * 73)
    for evt in events:
        lines.append(f"{evt['id']:<10} {evt['title'][:28]:<30} {evt['category']:<15} {evt['capacity']:<10} {evt['fee']:<8.2f}")
    lines.append("")

    lines.append("--- 3. PARTICIPANT ROSTER & PAYMENT STATUS ---")
    lines.append(f"{'Reg ID':<15} {'Name':<20} {'Event':<25} {'Status':<15} {'Paid ($)':<10}")
    lines.append("-" * 85)
    for p in participants:
        lines.append(f"{p['reg_id']:<15} {p['name'][:18]:<20} {p['event'][:23]:<25} {p['payment_status']:<15} {p['amount_paid']:<10.2f}")
    lines.append("")

    lines.append("=" * 70)
    lines.append("                       END OF REPORT")
    lines.append("=" * 70)

    content = "\n".join(lines)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True, filename, filepath
    except IOError as e:
        return False, str(e), None

def export_participants_csv():
    """
    Exports all participant data to a CSV spreadsheet file.
    Demonstrates Python standard csv module usage.
    """
    ensure_directories()
    filename = "participants_export.csv"
    filepath = os.path.join(REPORTS_DIR, filename)

    participants = get_all_participants()
    if not participants:
        return False, "No participant data available to export.", None

    headers = [
        "Registration ID", "Name", "Age", "Gender", "Organization",
        "Phone", "Email", "Event Title", "Fee", "Amount Paid",
        "Payment Status", "Payment Mode", "Attendance", "Certificate Status"
    ]

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for p in participants:
                writer.writerow([
                    p.get("reg_id", ""),
                    p.get("name", ""),
                    p.get("age", ""),
                    p.get("gender", ""),
                    p.get("organization", ""),
                    p.get("phone", ""),
                    p.get("email", ""),
                    p.get("event", ""),
                    p.get("fee", 0.0),
                    p.get("amount_paid", 0.0),
                    p.get("payment_status", ""),
                    p.get("payment_mode", ""),
                    p.get("attendance", ""),
                    p.get("certificate_eligible", "")
                ])
        return True, filename, filepath
    except IOError as e:
        return False, str(e), None

def list_report_files():
    """Lists all text and csv reports generated in reports folder."""
    ensure_directories()
    if not os.path.exists(REPORTS_DIR):
        return []
    return [f for f in os.listdir(REPORTS_DIR) if f.endswith(".txt") or f.endswith(".csv")]

def read_report_file(filename):
    """Reads content of a report text file."""
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        return "File not found."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        return f"Error reading file: {e}"
