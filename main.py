### library_management_system/
# This project contains both console and GUI versions of a Library Management System with SQLite integration.

# ----------------------
# FILE: db.py
# ----------------------
import sqlite3

def connect():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            isbn TEXT,
            quantity INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            course TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS issued (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_roll TEXT,
            book_id INTEGER,
            issue_date TEXT,
            return_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_book(title, author, isbn, quantity):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, isbn, quantity) VALUES (?, ?, ?, ?)",
                (title, author, isbn, quantity))
    conn.commit()
    conn.close()

def view_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

# ----------------------
# FILE: gui_main.py
# ----------------------
try:
    import tkinter as tk
    from tkinter import messagebox
    GUI_AVAILABLE = True
except ImportError:
    print("Tkinter is not available. GUI features will not work in this environment.")
    GUI_AVAILABLE = False

import db

db.connect()

if GUI_AVAILABLE:
    class LibraryGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Library Management System")
            self.root.geometry("600x400")

            self.title_label = tk.Label(root, text="Title")
            self.title_label.grid(row=0, column=0)
            self.title_entry = tk.Entry(root)
            self.title_entry.grid(row=0, column=1)

            self.author_label = tk.Label(root, text="Author")
            self.author_label.grid(row=1, column=0)
            self.author_entry = tk.Entry(root)
            self.author_entry.grid(row=1, column=1)

            self.isbn_label = tk.Label(root, text="ISBN")
            self.isbn_label.grid(row=2, column=0)
            self.isbn_entry = tk.Entry(root)
            self.isbn_entry.grid(row=2, column=1)

            self.quantity_label = tk.Label(root, text="Quantity")
            self.quantity_label.grid(row=3, column=0)
            self.quantity_entry = tk.Entry(root)
            self.quantity_entry.grid(row=3, column=1)

            self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
            self.add_button.grid(row=4, column=1)

            self.view_button = tk.Button(root, text="View Books", command=self.view_books)
            self.view_button.grid(row=4, column=2)

            self.books_listbox = tk.Listbox(root, width=80)
            self.books_listbox.grid(row=5, column=0, columnspan=4)

        def add_book(self):
            title = self.title_entry.get()
            author = self.author_entry.get()
            isbn = self.isbn_entry.get()
            quantity = self.quantity_entry.get()

            if title and quantity.isdigit():
                db.insert_book(title, author, isbn, int(quantity))
                messagebox.showinfo("Success", "Book added successfully!")
                self.view_books()
            else:
                messagebox.showerror("Error", "Please enter valid book information.")

        def view_books(self):
            self.books_listbox.delete(0, tk.END)
            for row in db.view_books():
                self.books_listbox.insert(tk.END, row)

    if __name__ == '__main__':
        root = tk.Tk()
        app = LibraryGUI(root)
        root.mainloop()
else:
    if __name__ == '__main__':
        print("GUI cannot be displayed. Please use console_version.py or install Tkinter.")

# ----------------------
# FILE: console_version.py
# ----------------------
import db

def main_menu():
    db.connect()
    while True:
        print("\n--- Library Management ---")
        print("1. Add Book")
        print("2. View Books")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            quantity = input("Enter quantity: ")
            if title and quantity.isdigit():
                db.insert_book(title, author, isbn, int(quantity))
                print("Book added successfully!")
            else:
                print("Invalid input.")
        elif choice == '2':
            books = db.view_books()
            for b in books:
                print(b)
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main_menu()
