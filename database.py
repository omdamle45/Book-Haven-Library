import json
import os
import threading

# --- AUTOMATIC PATH FIX ---
# This ensures the file is created in the EXACT same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.join(BASE_DIR, "media_store.json")

_LOCK = threading.Lock()
ALLOWED_CATEGORIES = ["Book", "Film", "Magazine"]

def _init_store():
    """Creates the file if it doesn't exist OR if it is empty/corrupted."""
    should_create = False
    
    # Check 1: Does file exist?
    if not os.path.exists(STORE_FILE):
        should_create = True
    else:
        # Check 2: Is file empty? (0 bytes)
        if os.path.getsize(STORE_FILE) == 0:
            should_create = True

    if should_create:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump({"next_id": 1, "items": {}}, f, indent=2)

def _load():
    """Safe load function that handles corrupted files."""
    _init_store()
    with _LOCK:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"next_id": 1, "items": {}}

def _save(data):
    with _LOCK:
        with open(STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def list_all():
    data = _load()
    return list(data["items"].values())

def list_by_category(category):
    return [m for m in list_all() if m["category"] == category]

# --- SMART SEARCH (Partial Match) ---
def search_smart(query):
    query = query.lower().strip()
    if not query: return list_all()
    # Searches in Name AND Author for better results
    return [m for m in list_all() if query in m["name"].lower() or query in m.get("author", "").lower()]

def search_exact(name):
    return [m for m in list_all() if m["name"] == name]

def get_item(item_id):
    data = _load()
    return data["items"].get(str(item_id))

def create_item(name, publication_date, author, category):
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category. Allowed: {ALLOWED_CATEGORIES}")
    
    data = _load()
    item_id = data["next_id"]
    item = {
        "id": item_id,
        "name": name,
        "publication_date": publication_date,
        "author": author,
        "category": category,
        "status": "Available",     # Default status
        "borrow_date": None,       # New field
        "borrower": None           # New field
    }
    data["items"][str(item_id)] = item
    data["next_id"] += 1
    _save(data)
    return item

def update_item(item_id, name, pub, auth, cat):
    data = _load()
    key = str(item_id)
    if key in data["items"]:
        data["items"][key]["name"] = name
        data["items"][key]["publication_date"] = pub
        data["items"][key]["author"] = auth
        data["items"][key]["category"] = cat
        _save(data)
        return data["items"][key]
    return None

# --- STATUS UPDATE (Borrow/Return) ---
def set_status(item_id, new_status, borrow_date=None, borrower=None):
    data = _load()
    key = str(item_id)
    if key in data["items"]:
        data["items"][key]["status"] = new_status
        data["items"][key]["borrow_date"] = borrow_date
        data["items"][key]["borrower"] = borrower
        _save(data)
        return data["items"][key]
    return None

def delete_item(item_id):
    data = _load()
    key = str(item_id)
    if key in data["items"]:
        del data["items"][key]
        _save(data)
        return True
    return False