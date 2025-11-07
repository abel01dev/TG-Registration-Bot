import json
import os

DATA_FILE = "data.json"

def load_data():
    """Load existing registrations from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    """Save all registration data to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def generate_user_id(data):
    """Generate a unique user ID like USR-001, USR-002, etc."""
    if not data:
        return "USR-001"
    # Find the last numeric part of the latest user ID
    last_user = data[-1]
    last_id = last_user.get("id", "USR-000")
    try:
        last_num = int(last_id.split("-")[1])
    except (IndexError, ValueError):
        last_num = 0
    new_id = f"USR-{last_num + 1:03d}"
    return new_id

def add_user(name, phone):
    """Add a new user's registration info with an auto-generated ID."""
    data = load_data()
    user_id = generate_user_id(data)
    user_entry = {
        "id": user_id,
        "name": name,
        "phone": phone
    }
    data.append(user_entry)
    save_data(data)
    return user_id
