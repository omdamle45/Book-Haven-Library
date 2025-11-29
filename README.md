# Advanced Book Store (Media Library)

## About the Book Store
A simple, local media library that manages Books, Films, and Magazines. It provides:
- A Flask backend for CRUD operations on media items.
- A modern Tkinter GUI to browse, search, filter, add, edit, and delete items.
- Persistent storage in a JSON file (media_store.json), no external DB required.

## What You Need to Start
Prerequisites:
- Python 3.9+ installed
- Internet access to install dependencies
- Basic familiarity with running Python scripts

Setup:
1. (Optional) Create and activate a virtual environment.
2. Install dependencies:
   - pip install flask flask-cors requests
3. Ensure all project files are in the same folder:
   - backend.py, frontend.py, database.py, media_store.json (auto-created)

## How to Run
Backend (starts on http://127.0.0.1:8000):
- python backend.py

Frontend (in another terminal):
- python frontend.py

## Features
- Modern Tkinter GUI (Book Haven Manager).
- List all media with ID, Name, Category, Author.
- Filter by category (All, Book, Film, Magazine).
- Exact name search.
- View detailed metadata with category icon.
- Create, edit, and delete media (POST/PUT/DELETE).
- Persistent JSON file media_store.json auto-created.

## API Endpoints
GET /media  
GET /media/category/<category>  
GET /media/search?name=ExactName  
GET /media/<id>  
POST /media  (JSON: name, publication_date, author, category)  
PUT /media/<id>  (JSON: name, publication_date, author, category)  
DELETE /media/<id>

## What Is Needed / Recommendations
- Input validation (dates, required fields, category whitelist).
- Error handling and user feedback (network errors, backend exceptions).
- Basic authentication if multi-user or network-exposed.
- Packaging: requirements.txt and optional installer script.
- Testing: unit tests for database.py and API routes.
- Data backup/restore for media_store.json.
- Optional enhancements: pagination, fuzzy search, export/import CSV/JSON.
