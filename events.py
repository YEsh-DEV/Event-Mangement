from utils import EVENTS_FILE, load_json, save_json

def get_all_events():
    """
    Retrieves all created events from local storage.
    Deserializes json array into python dictionaries list.
    """
    return load_json(EVENTS_FILE, [])

def save_events(events):
    """
    Saves the list of all events back to local JSON storage.
    Serializes list of dictionaries.
    """
    return save_json(EVENTS_FILE, events)

def get_event_by_title(title):
    """Finds an event by its title."""
    events = get_all_events()
    for evt in events:
        if evt["title"].strip().lower() == title.strip().lower():
            return evt
    return None

def get_event_by_id(event_id):
    """Finds an event by its unique ID."""
    events = get_all_events()
    for evt in events:
        if evt["id"] == event_id:
            return evt
    return None

def get_event_titles():
    """Returns a list of all event titles for UI dropdown menus."""
    events = get_all_events()
    return [evt["title"] for evt in events]

def add_event(title, category, date, time_str, venue, capacity, fee):
    """
    Creates and saves a new event.
    Demonstrates conditionals, type parsing, ID generation, and list operations.
    """
    if not title or not category or not date or not time_str or not venue:
        return False, "All fields are required."

    # Validate numeric fields
    try:
        cap_int = int(capacity)
        if cap_int <= 0:
            return False, "Capacity must be greater than 0."
    except ValueError:
        return False, "Capacity must be a valid integer."

    try:
        fee_float = float(fee)
        if fee_float < 0:
            return False, "Fee cannot be negative."
    except ValueError:
        return False, "Fee must be a valid number."

    events = get_all_events()
    
    # Check for duplicate event title
    if get_event_by_title(title):
        return False, f"An event named '{title}' already exists."

    # Generate Event ID
    event_id = f"EVT-{len(events) + 101}"

    new_event = {
        "id": event_id,
        "title": title.strip(),
        "category": category.strip(),
        "date": date.strip(),
        "time": time_str.strip(),
        "venue": venue.strip(),
        "capacity": cap_int,
        "fee": fee_float,
        "status": "Upcoming"
    }

    events.append(new_event)
    if save_events(events):
        return True, f"Event '{title}' created successfully! (ID: {event_id})"
    return False, "Failed to save event data."

def update_event(event_id, title, category, date, time_str, venue, capacity, fee):
    """Updates an existing event's details."""
    events = get_all_events()
    for i in range(len(events)):
        if events[i]["id"] == event_id:
            try:
                cap_int = int(capacity)
                fee_float = float(fee)
            except ValueError:
                return False, "Invalid capacity or fee value."

            events[i]["title"] = title.strip()
            events[i]["category"] = category.strip()
            events[i]["date"] = date.strip()
            events[i]["time"] = time_str.strip()
            events[i]["venue"] = venue.strip()
            events[i]["capacity"] = cap_int
            events[i]["fee"] = fee_float

            save_events(events)
            return True, "Event updated successfully!"

    return False, "Event not found."

def delete_event(event_id):
    """Deletes an event by ID."""
    events = get_all_events()
    for i in range(len(events)):
        if events[i]["id"] == event_id:
            del events[i]
            save_events(events)
            return True, "Event deleted successfully."
    return False, "Event not found."
