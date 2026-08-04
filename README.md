# Event Management System

## Project Overview
The **Event Management System** is a modern desktop software application built in Python designed to streamline event organizing, participant registration, payment tracking, attendance logging, analytical reporting, and data exporting.

This project was developed as a comprehensive Python university course project demonstrating fundamental and intermediate concepts covered in the Python programming syllabus.

---

## Key Features

1. **Event Management**: Create, view, update, and delete events. Each event features customizable title, category, venue, date, time, capacity limit, and registration fee.
2. **Participant Registration**: Register attendees with validation for contact details. Prevents overbooking by enforcing dynamic event seat capacity limits. Generates unique Registration IDs (`REG-2026-XXXX`).
3. **Payment Tracking & Dues**: Record payment transactions with multiple payment modes (`UPI`, `Cash`, `Credit/Debit Card`). Automatically categorizes statuses (`Paid`, `Partially Paid`, `Pending`) and tracks remaining dues.
4. **Attendance & Certificate Verification**: Log participant presence (`Present` / `Absent`). Enforces automated rules for Certificate Eligibility (Requires 100% Fee Paid AND Present status).
5. **Participant Analytics**: Interactive dashboard presenting key metrics (Total Revenue, Outstanding Dues, Fee Collection Rate %, Occupancy Rate, Gender Demographics, Category Distribution, Top Grossing Event).
6. **Report Generation & Data Export**: Generate timestamped plain text summary reports (`.txt`) and export structured participant records to CSV spreadsheets (`.csv`).

---

## Folder Architecture

```
event_management_app/
├── main.py            # Application entry point
├── ui.py              # Main GUI application window (CustomTkinter)
├── events.py          # Event creation, capacity checking, and list management
├── registration.py    # Participant registration, search, and validation
├── payments.py        # Payment processing, dues calculation, and transaction recording
├── attendance.py      # Attendance logging and certificate eligibility rules
├── analytics.py       # Analytics aggregation engine (revenue, demographics, popular events)
├── reports.py         # Text report formatter and CSV exporter
├── utils.py           # JSON file handler, regex validators, and sample seed data
├── requirements.txt   # Required Python packages (customtkinter)
├── data/              # Auto-created storage folder (events.json, participants.json)
├── reports/           # Auto-created export folder (.txt and .csv reports)
└── README.md          # Project documentation and viva guide
```

---

## Python Syllabus Concepts Demonstrated

- **Variables & Data Types**: Strings, integers, floats, booleans, and datetime timestamps.
- **Control Flow**: `if-elif-else` conditional logic for validation, payment status, and certificate rules; `for` and `while` loops for dataset searching and aggregation.
- **Data Structures**:
  - **Lists**: Storing collections of event and participant records.
  - **Dictionaries**: Structuring individual participant and event attributes.
  - **Tuples**: Returning multiple status values from functions `(True, "Success message")`.
  - **Sets**: Extracting unique category names and event titles.
- **Functions & Modular Design**: Standard user-defined functions across specialized modules.
- **File Handling**: JSON data storage (`json.dump`, `json.load`), text report generation (`open()`, `.write()`), and CSV exporting (`csv.writer`).
- **Exception Handling**: `try-except` blocks for numeric parsing (`ValueError`), file errors (`IOError`), and regex validation.
- **Object-Oriented Programming (OOP)**: Class structures for GUI application widgets (`ctk.CTk`).
- **Modules & Libraries**: Standard (`os`, `json`, `csv`, `re`, `random`, `datetime`, `tkinter`, `ttk`) and external (`customtkinter`).

---

## Quick Start Guide

### 1. Requirements
Ensure Python 3.8+ is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python main.py
```

---

## Viva / Explanation Reference Guide

1. **How is data persisted when the app closes?**
   - Data is stored in JSON files (`data/events.json` and `data/participants.json`) using `json.dump()` and loaded via `json.load()` upon startup in `utils.py`.

2. **How does dynamic capacity validation work?**
   - In `registration.py`, `get_event_enrollment_count()` iterates through all participants registered for an event. If the count reaches `event["capacity"]`, registration is blocked with a user warning.

3. **How is Certificate Eligibility computed?**
   - In `attendance.py` and `payments.py`, eligibility is dynamically set to `"Eligible"` only when `attendance == "Present"` AND `payment_status == "Paid"`.

4. **How are reports exported?**
   - Plain text reports are formatted with string alignments and written to `reports/event_report_TIMESTAMP.txt`. CSV files are generated using Python's built-in `csv` library into `reports/participants_export.csv`.
