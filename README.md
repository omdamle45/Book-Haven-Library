# Book Haven: Library Manager

Book Haven is a desktop application built with Python to help manage a small library's inventory (books, films, magazines) and track borrowing activity.

The system is designed with a clear separation of tasks: a **server** handles the core logic and data, and a **desktop application** provides the visual interface.

---

## What the Program Does

The application offers several core functions for efficient library management:

* **Borrow and Return:** Easily check out items to patrons, record their names, and update the item status when it's returned.
* **Filter Items:** Users can quickly narrow the main list to show only **Books**, **Films**, or **Magazines**, making search faster.
* **Edit Records:** You can correct or update the details (like the author or title) of any media item already in the library.
* **View Statistics:** Provides a real-time summary of the current inventory, including totals and the number of items currently checked out.
* **Add New Media:** A dedicated form allows staff to add new items to the library collection.

---

## How It Works (Technical Overview)

The system uses a standard **Client-Server** model written entirely in Python. 

| Component | Technology | Role |
| :--- | :--- | :--- |
| **The Desktop App** | **Python Tkinter** | The visual program that users interact with. It sends requests (messages) to the Server. |
| **The Server** | **Python Flask** | This runs in the background. It manages all the business rules (like loan limits) and controls the database. |
| **The Database** | **JSON File** | A simple file used to permanently save all of the library's inventory and loan data. |

---

## Simple Setup Guide

You must start the **Server first**, then the **Desktop Application**.

1.  **Install Python** (Version 3.10 or newer).
2.  **Install required tools** (Flask and Requests):
    ```bash
    pip install flask requests
    ```
3.  **Start the Server (Backend):** Open a command line/terminal and run:
    ```bash
    python backend.py
    ```
    *(Keep this window open and running.)*
4.  **Run the Desktop App (Frontend):** Open a second command line/terminal and run:
    ```bash
    python frontend.py
    ```
    *The app window will now open and connect to the running server.*