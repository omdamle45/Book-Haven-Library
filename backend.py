from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date
import database  # Imports your database.py file

app = Flask(__name__)
CORS(app)

# --- STANDARD ENDPOINTS ---

@app.route("/media", methods=["GET"])
def get_all():
    return jsonify(database.list_all())

@app.route("/media", methods=["POST"])
def create():
    d = request.json
    new_item = database.create_item(
        name=d.get("name"), 
        publication_date=d.get("publication_date"), 
        author=d.get("author"), 
        category=d.get("category")
    )
    return jsonify(new_item), 201

@app.route("/media/category/<cat>", methods=["GET"])
def get_by_cat(cat):
    return jsonify(database.list_by_category(cat))

@app.route("/media/search", methods=["GET"])
def search():
    name = request.args.get("name", "")
    return jsonify(database.search_smart(name))

@app.route("/media/<int:id>", methods=["GET"])
def get_one(id):
    item = database.get_item(id)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route("/media/<int:id>", methods=["PUT"])
def update(id):
    d = request.json
    updated_item = database.update_item(
        item_id=id,
        name=d.get("name"),
        pub=d.get("publication_date"),
        auth=d.get("author"),
        cat=d.get("category")
    )
    if updated_item:
        return jsonify(updated_item)
    return jsonify({"error": "Not found"}), 404

@app.route("/media/<int:id>", methods=["DELETE"])
def delete(id):
    if database.delete_item(id):
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Not found"}), 404

# --- SPECIAL FEATURES (Borrow, Return, Stats) ---

@app.route("/media/<int:id>/borrow", methods=["POST"])
def borrow_item(id):
    """Mark item as Checked Out with Name AND Date"""
    data = request.json
    borrower_name = data.get("borrower", "Unknown")
    
    # Use provided date or default to today
    borrow_date = data.get("borrow_date")
    if not borrow_date:
        borrow_date = date.today().isoformat()
    
    item = database.set_status(id, "Checked Out", borrow_date, borrower_name)
    
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route("/media/<int:id>/return", methods=["POST"])
def return_item(id):
    """Mark item as Available"""
    item = database.set_status(id, "Available", None, None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

@app.route("/stats", methods=["GET"])
def get_stats():
    items = database.list_all()
    stats = {
        "total": len(items), 
        "Book": 0, 
        "Film": 0, 
        "Magazine": 0, 
        "Borrowed": 0
    }
    
    for item in items:
        cat = item.get("category", "Book")
        if cat in stats: 
            stats[cat] += 1
        
        if item.get("status") == "Checked Out":
            stats["Borrowed"] += 1
            
    return jsonify(stats)

if __name__ == "__main__":
    database._init_store()
    print("Backend Server Running on http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)