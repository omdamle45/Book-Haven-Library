import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import date # To autofill today's date

API_URL = "http://127.0.0.1:8000"

# --- COLORS & FONTS ---
BG_COLOR = "#F0F2F5"
HEADER_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"
EDIT_COLOR = "#F39C12"
BORROW_COLOR = "#2ECC71"
RETURN_COLOR = "#E67E22"
TEXT_COLOR = "#333333"
FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_HEADER = ("Segoe UI", 14, "bold")

class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Haven Library")
        self.geometry("1100x700")
        self.configure(bg=BG_COLOR)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=FONT_MAIN, borderwidth=0)
        style.configure("Treeview.Heading", background="#EAECEF", font=FONT_BOLD, borderwidth=0)
        style.map("Treeview", background=[("selected", ACCENT_COLOR)])
        style.configure("TButton", font=FONT_MAIN, padding=6)
        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground="white", font=FONT_BOLD)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # HEADER
        header = tk.Frame(self, bg=HEADER_COLOR, height=60)
        header.pack(fill="x")
        tk.Label(header, text="📚 Book Haven Manager", bg=HEADER_COLOR, fg="white", font=FONT_HEADER).pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="+ Add New Media", bg="#27AE60", fg="white", font=FONT_BOLD, bd=0, padx=15, pady=5, cursor="hand2", command=self.open_add_window).pack(side="right", padx=20, pady=12)
        tk.Button(header, text="📊 View Stats", bg="#8E44AD", fg="white", font=FONT_BOLD, bd=0, padx=15, pady=5, cursor="hand2", command=self.show_stats).pack(side="right", padx=5, pady=12)

        # MAIN LAYOUT
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # LEFT PANEL
        left_panel = tk.Frame(main_container, bg=BG_COLOR)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Filter Bar
        filter_frame = tk.Frame(left_panel, bg=BG_COLOR)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter:", bg=BG_COLOR, font=FONT_BOLD).pack(side="left")
        self.cat_var = tk.StringVar(value="All")
        cb = ttk.Combobox(filter_frame, textvariable=self.cat_var, values=["All", "Book", "Film", "Magazine"], state="readonly", width=12)
        cb.pack(side="left", padx=10)
        cb.bind("<<ComboboxSelected>>", self.filter)

        tk.Label(filter_frame, text="Search:", bg=BG_COLOR, font=FONT_BOLD).pack(side="left", padx=(20, 0))
        self.search_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.search_var, font=FONT_MAIN, width=20, bd=1, relief="solid").pack(side="left", padx=10)
        tk.Button(filter_frame, text="Go", bg=ACCENT_COLOR, fg="white", bd=0, padx=10, command=self.search).pack(side="left")
        tk.Button(filter_frame, text="↻ Reset", bg="#95A5A6", fg="white", bd=0, padx=10, command=self.load_data).pack(side="left", padx=5)

        # The List (Treeview)
        tree_frame = tk.Frame(left_panel, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("ID", "Name", "Category", "Author", "Date", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID", anchor="w"); self.tree.column("ID", width=40, anchor="w")
        self.tree.heading("Name", text="Name", anchor="w"); self.tree.column("Name", width=200, anchor="w")
        self.tree.heading("Category", text="Type", anchor="w"); self.tree.column("Category", width=80, anchor="w")
        self.tree.heading("Author", text="Author", anchor="w"); self.tree.column("Author", width=150, anchor="w")
        self.tree.heading("Date", text="Date", anchor="w"); self.tree.column("Date", width=100, anchor="w")
        self.tree.heading("Status", text="Status", anchor="w"); self.tree.column("Status", width=100, anchor="w")
        
        self.tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # RIGHT PANEL: Details
        self.right_panel = tk.Frame(main_container, bg="white", width=320, bd=1, relief="solid")
        self.right_panel.pack(side="right", fill="y", padx=(10, 0))
        self.right_panel.pack_propagate(False)

        tk.Label(self.right_panel, text="Item Details", bg="white", fg=ACCENT_COLOR, font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
        self.lbl_icon = tk.Label(self.right_panel, text="📖", bg="white", font=("Arial", 40))
        self.lbl_icon.pack(pady=10)
        self.lbl_name = tk.Label(self.right_panel, text="Select an item", bg="white", font=("Segoe UI", 12, "bold"), wraplength=280)
        self.lbl_name.pack(pady=5)
        self.lbl_meta = tk.Label(self.right_panel, text="", bg="white", font=FONT_MAIN, fg="#666666", justify="center")
        self.lbl_meta.pack(pady=5)
        
        self.lbl_status = tk.Label(self.right_panel, text="", bg="white", font=FONT_BOLD, fg="#27AE60", wraplength=280)
        self.lbl_status.pack(pady=5)

        # Action Buttons
        self.btn_borrow = tk.Button(self.right_panel, text="Borrow Item", bg=BORROW_COLOR, fg="white", font=FONT_BOLD, bd=0, padx=20, pady=8, cursor="hand2", command=self.open_borrow_window, state="disabled")
        self.btn_borrow.pack(side="top", pady=(20, 5), padx=20, fill="x")

        self.btn_return = tk.Button(self.right_panel, text="Return Item", bg=RETURN_COLOR, fg="white", font=FONT_BOLD, bd=0, padx=20, pady=8, cursor="hand2", command=self.return_item, state="disabled")
        self.btn_return.pack(side="top", pady=(0, 5), padx=20, fill="x")

        self.btn_edit = tk.Button(self.right_panel, text="Edit Details", bg=EDIT_COLOR, fg="white", font=FONT_BOLD, bd=0, padx=20, pady=8, cursor="hand2", command=self.open_edit_window, state="disabled")
        self.btn_edit.pack(side="top", pady=(0, 5), padx=20, fill="x")
        
        self.btn_del = tk.Button(self.right_panel, text="Delete Item", bg="#E74C3C", fg="white", font=FONT_BOLD, bd=0, padx=20, pady=8, cursor="hand2", command=self.delete, state="disabled")
        self.btn_del.pack(side="bottom", pady=20, padx=20, fill="x")

    # --- LOGIC ---
    def load_data(self):
        try:
            self.populate(requests.get(f"{API_URL}/media").json())
        except: messagebox.showerror("Connection Error", "Is backend.py running?")

    def populate(self, items):
        self.tree.delete(*self.tree.get_children())
        for i in items:
            status = i.get("status", "Available")
            self.tree.insert("", "end", values=(i["id"], i["name"], i["category"], i["author"], i.get("publication_date", ""), status))

    def filter(self, e):
        c = self.cat_var.get()
        url = f"{API_URL}/media" if c == "All" else f"{API_URL}/media/category/{c}"
        self.populate(requests.get(url).json())

    def search(self):
        name = self.search_var.get()
        if not name: return self.load_data()
        self.populate(requests.get(f"{API_URL}/media/search", params={"name": name}).json())

    def on_select(self, e):
        sel = self.tree.selection()
        if not sel: return
        item_id = self.tree.item(sel[0])['values'][0]
        data = requests.get(f"{API_URL}/media/{item_id}").json()
        
        self.lbl_name.config(text=data['name'])
        self.lbl_meta.config(text=f"Author: {data['author']}\nCategory: {data['category']}\nPublished: {data['publication_date']}")
        
        # --- SHOW BORROWER INFO ---
        status = data.get("status", "Available")
        borrower = data.get("borrower")
        date_txt = data.get("borrow_date")
        
        if status == "Checked Out":
            msg = f"🔴 Checked Out\nBy: {borrower}\nSince: {date_txt}"
            self.lbl_status.config(text=msg, fg="#E74C3C")
            self.btn_borrow.config(state="disabled")
            self.btn_return.config(state="normal")
        else:
            self.lbl_status.config(text="🟢 Available", fg="#27AE60")
            self.btn_borrow.config(state="normal")
            self.btn_return.config(state="disabled")

        self.lbl_icon.config(text="🎬" if data['category'] == "Film" else "📰" if data['category'] == "Magazine" else "📖")
        self.btn_del.config(state="normal")
        self.btn_edit.config(state="normal")

    def open_borrow_window(self):
        """Opens popup to enter Borrower Name and Date"""
        if not self.tree.selection(): return
        item_id = self.tree.item(self.tree.selection()[0])['values'][0]
        
        top = tk.Toplevel(self)
        top.title("Borrow Item")
        top.geometry("350x250")
        top.configure(bg="white")
        
        tk.Label(top, text="Borrower Name:", bg="white", font=FONT_BOLD).pack(anchor="w", padx=20, pady=(20,0))
        name_entry = tk.Entry(top, bd=1, relief="solid", font=FONT_MAIN)
        name_entry.pack(fill="x", padx=20, pady=5)
        
        tk.Label(top, text="Borrow Date (YYYY-MM-DD):", bg="white", font=FONT_BOLD).pack(anchor="w", padx=20, pady=(10,0))
        date_entry = tk.Entry(top, bd=1, relief="solid", font=FONT_MAIN)
        date_entry.insert(0, date.today().isoformat()) # Auto-fill today
        date_entry.pack(fill="x", padx=20, pady=5)
        
        def confirm():
            if not name_entry.get():
                messagebox.showwarning("Error", "Name is required")
                return
            
            # Send name AND date to backend
            requests.post(f"{API_URL}/media/{item_id}/borrow", json={
                "borrower": name_entry.get(),
                "borrow_date": date_entry.get()
            })
            self.load_data()
            self.on_select(None)
            top.destroy()
            
        tk.Button(top, text="Confirm Borrow", bg=BORROW_COLOR, fg="white", font=FONT_BOLD, bd=0, command=confirm).pack(fill="x", padx=20, pady=20)

    def return_item(self):
        requests.post(f"{API_URL}/media/{self.tree.item(self.tree.selection()[0])['values'][0]}/return")
        self.load_data(); self.on_select(None)

    def show_stats(self):
        try:
            stats = requests.get(f"{API_URL}/stats").json()
            msg = f"📚 Total Items: {stats['total']}\n\n" \
                  f"📖 Books: {stats['Book']}\n" \
                  f"🎬 Films: {stats['Film']}\n" \
                  f"📰 Magazines: {stats['Magazine']}\n\n" \
                  f"🔴 Currently Borrowed: {stats['Borrowed']}"
            messagebox.showinfo("Library Statistics", msg)
        except:
            messagebox.showerror("Error", "Could not fetch stats.")

    def delete(self):
        if messagebox.askyesno("Confirm", "Delete this item?"):
            requests.delete(f"{API_URL}/media/{self.tree.item(self.tree.selection()[0])['values'][0]}")
            self.load_data()
            self.reset_details()

    def reset_details(self):
        self.lbl_name.config(text="Select an item")
        self.lbl_meta.config(text="")
        self.lbl_status.config(text="")
        self.lbl_icon.config(text="📖")
        self.btn_del.config(state="disabled")
        self.btn_edit.config(state="disabled")
        self.btn_borrow.config(state="disabled")
        self.btn_return.config(state="disabled")

    def open_add_window(self):
        self.form_window("Add Media", {}, self.save_new)

    def open_edit_window(self):
        if not self.tree.selection(): return
        item_id = self.tree.item(self.tree.selection()[0])['values'][0]
        data = requests.get(f"{API_URL}/media/{item_id}").json()
        self.form_window(f"Edit Media #{item_id}", data, lambda p: self.save_edit(item_id, p))

    def form_window(self, title, data, save_cb):
        top = tk.Toplevel(self)
        top.title(title)
        top.geometry("350x380")
        top.configure(bg="white")
        
        def entry(lbl, val=""):
            tk.Label(top, text=lbl, bg="white", font=FONT_BOLD).pack(anchor="w", padx=20, pady=(10,0))
            e = tk.Entry(top, bd=1, relief="solid", font=FONT_MAIN)
            e.insert(0, val)
            e.pack(fill="x", padx=20, pady=5)
            return e

        n = entry("Name", data.get("name", ""))
        a = entry("Author", data.get("author", ""))
        d = entry("Date (YYYY-MM-DD)", data.get("publication_date", ""))
        
        tk.Label(top, text="Category", bg="white", font=FONT_BOLD).pack(anchor="w", padx=20, pady=(10,0))
        c = ttk.Combobox(top, values=["Book", "Film", "Magazine"], state="readonly")
        c.set(data.get("category", "Book"))
        c.pack(fill="x", padx=20, pady=5)

        def submit():
            if not n.get() or not a.get(): return messagebox.showwarning("Error", "Name/Author required")
            save_cb({
                "name": n.get(), "author": a.get(), "publication_date": d.get(), "category": c.get()
            })
            top.destroy()

        tk.Button(top, text="Save", bg=ACCENT_COLOR, fg="white", font=FONT_BOLD, bd=0, command=submit, pady=8).pack(fill="x", padx=20, pady=20)

    def save_new(self, payload):
        requests.post(f"{API_URL}/media", json=payload)
        self.load_data()

    def save_edit(self, item_id, payload):
        requests.put(f"{API_URL}/media/{item_id}", json=payload)
        self.load_data()
        self.on_select(None) # Refresh details view

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()