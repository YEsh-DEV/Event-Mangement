import random
from events import get_all_events
from registration import get_all_participants

ANALYTICS_TIPS = [
    "Tip: Automated payment tracking reduces registration drop-off by up to 25%.",
    "Tip: Early bird registration discounts help lock in minimum event capacity early.",
    "Tip: Send automated SMS/Email reminders 24 hours before the event to maximize attendance.",
    "Tip: Certificates should only be issued after confirming 100% payment clearance.",
    "Tip: Venue capacity buffer of 10% accounts for last-minute VIP or organizer entries.",
    "Tip: Track category metrics to see whether Technology or Workshop events perform better.",
    "Tip: Offer multiple payment options (UPI, Card, Cash) to accelerate fee collection."
]

def get_random_insight():
    """
    Returns a random event management tip or best practice tip.
    Uses random.choice to query tips list.
    """
    return random.choice(ANALYTICS_TIPS)

def generate_full_analytics():
    """
    Computes comprehensive analytics across events, participants, payments, and demographics.
    Demonstrates data aggregation, dictionary manipulation, sorting, and math functions.
    """
    events = get_all_events()
    participants = get_all_participants()

    total_events = len(events)
    total_participants = len(participants)
    total_capacity = sum(evt.get("capacity", 0) for evt in events)

    occupancy_rate = (total_participants / total_capacity * 100) if total_capacity > 0 else 0.0

    total_fee_expected = sum(p.get("fee", 0.0) for p in participants)
    total_revenue_collected = sum(p.get("amount_paid", 0.0) for p in participants)
    outstanding_dues = total_fee_expected - total_revenue_collected
    collection_rate = (total_revenue_collected / total_fee_expected * 100) if total_fee_expected > 0 else 0.0

    # Enrollments and revenue by event
    event_counts = {}
    event_revenues = {}
    for p in participants:
        evt_title = p.get("event", "Unknown")
        event_counts[evt_title] = event_counts.get(evt_title, 0) + 1
        event_revenues[evt_title] = event_revenues.get(evt_title, 0.0) + p.get("amount_paid", 0.0)

    most_popular_event = "N/A"
    most_popular_count = 0
    if event_counts:
        most_popular_event = max(event_counts, key=event_counts.get)
        most_popular_count = event_counts[most_popular_event]

    top_revenue_event = "N/A"
    top_revenue_amount = 0.0
    if event_revenues:
        top_revenue_event = max(event_revenues, key=event_revenues.get)
        top_revenue_amount = event_revenues[top_revenue_event]

    # Category breakdown
    category_counts = {}
    evt_category_map = {evt["title"]: evt["category"] for evt in events}
    for p in participants:
        cat = evt_category_map.get(p.get("event"), "General")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Gender breakdown
    gender_counts = {}
    for p in participants:
        g = p.get("gender", "Other")
        gender_counts[g] = gender_counts.get(g, 0) + 1

    # Payment status breakdown
    payment_counts = {"Paid": 0, "Partially Paid": 0, "Pending": 0}
    for p in participants:
        status = p.get("payment_status", "Pending")
        payment_counts[status] = payment_counts.get(status, 0) + 1

    return {
        "total_events": total_events,
        "total_participants": total_participants,
        "total_capacity": total_capacity,
        "occupancy_rate": occupancy_rate,
        "total_fee_expected": total_fee_expected,
        "total_revenue_collected": total_revenue_collected,
        "outstanding_dues": outstanding_dues,
        "collection_rate": collection_rate,
        "most_popular_event": most_popular_event,
        "most_popular_count": most_popular_count,
        "top_revenue_event": top_revenue_event,
        "top_revenue_amount": top_revenue_amount,
        "category_counts": category_counts,
        "gender_counts": gender_counts,
        "payment_counts": payment_counts,
        "random_insight": get_random_insight()
    }
