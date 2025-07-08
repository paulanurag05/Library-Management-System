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
            return_date TEXT,
            FOREIGN KEY(student_roll) REFERENCES students(roll),
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# Book Functions
# -------------------------------
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

def get_book_by_title(title):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title=?", (title,))
    row = cur.fetchone()
    conn.close()
    return row

def update_book_quantity(book_id, delta):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET quantity = quantity + ? WHERE id=?", (delta, book_id))
    conn.commit()
    conn.close()

# -------------------------------
# Student Functions
# -------------------------------
def insert_student(name, roll, course):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, roll, course) VALUES (?, ?, ?)", (name, roll, course))
    conn.commit()
    conn.close()

def view_students():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_student_rolls():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT roll FROM students")
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows

# -------------------------------
# Book Issue/Return Functions
# -------------------------------
def issue_book(student_roll, book_id, issue_date, return_date):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO issued (student_roll, book_id, issue_date, return_date) VALUES (?, ?, ?, ?)",
                (student_roll, book_id, issue_date, return_date))
    update_book_quantity(book_id, -1)  # Reduce quantity
    conn.commit()
    conn.close()

def return_book(issue_id, book_id):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM issued WHERE id=?", (issue_id,))
    update_book_quantity(book_id, 1)  # Increase quantity
    conn.commit()
    conn.close()

def view_issued_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT issued.id, students.name, students.roll, books.title, issued.issue_date, issued.return_date
        FROM issued
        JOIN students ON issued.student_roll = students.roll
        JOIN books ON issued.book_id = books.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
