import db
db.connect()

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    from datetime import datetime
except ImportError:
    print("Tkinter not available.")
    exit()

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")

        tab_control = ttk.Notebook(self.root)
        book_tab = ttk.Frame(tab_control)
        student_tab = ttk.Frame(tab_control)
        issue_tab = ttk.Frame(tab_control)
        tab_control.add(book_tab, text='📚 Books')
        tab_control.add(student_tab, text='👨‍🎓 Students')
        tab_control.add(issue_tab, text='📦 Issue Book')
        tab_control.pack(expand=1, fill='both')

        # --- Book Tab ---
        book_form = ttk.Frame(book_tab, padding=10)
        book_form.pack(pady=10)

        ttk.Label(book_form, text="Title:").grid(row=0, column=0)
        self.title_entry = ttk.Entry(book_form, width=30)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(book_form, text="Author:").grid(row=1, column=0)
        self.author_entry = ttk.Entry(book_form, width=30)
        self.author_entry.grid(row=1, column=1)

        ttk.Label(book_form, text="ISBN:").grid(row=2, column=0)
        self.isbn_entry = ttk.Entry(book_form, width=30)
        self.isbn_entry.grid(row=2, column=1)

        ttk.Label(book_form, text="Quantity:").grid(row=3, column=0)
        self.quantity_entry = ttk.Entry(book_form, width=30)
        self.quantity_entry.grid(row=3, column=1)

        ttk.Button(book_form, text="Add Book", command=self.add_book).grid(row=4, column=0, pady=10)
        ttk.Button(book_form, text="View Books", command=self.view_books).grid(row=4, column=1)

        self.books_listbox = tk.Listbox(book_tab, font=("Courier New", 10), height=12, width=100)
        self.books_listbox.pack(padx=10, pady=10)

        # --- Student Tab ---
        student_form = ttk.Frame(student_tab, padding=10)
        student_form.pack()

        ttk.Label(student_form, text="Name:").grid(row=0, column=0)
        self.student_name = ttk.Entry(student_form, width=30)
        self.student_name.grid(row=0, column=1)

        ttk.Label(student_form, text="Roll No:").grid(row=1, column=0)
        self.student_roll = ttk.Entry(student_form, width=30)
        self.student_roll.grid(row=1, column=1)

        ttk.Label(student_form, text="Course:").grid(row=2, column=0)
        self.student_course = ttk.Entry(student_form, width=30)
        self.student_course.grid(row=2, column=1)

        ttk.Button(student_form, text="Register Student", command=self.register_student).grid(row=3, column=0, pady=10)
        ttk.Button(student_form, text="View Students", command=self.view_students).grid(row=3, column=1)

        self.students_listbox = tk.Listbox(student_tab, font=("Courier New", 10), height=10, width=80)
        self.students_listbox.pack(padx=10, pady=10)

        # --- Issue Tab ---
        issue_form = ttk.Frame(issue_tab, padding=10)
        issue_form.pack()

        ttk.Label(issue_form, text="Select Student Roll:").grid(row=0, column=0)
        self.roll_combo = ttk.Combobox(issue_form, values=db.get_student_rolls(), width=30)
        self.roll_combo.grid(row=0, column=1)

        ttk.Label(issue_form, text="Select Book Title:").grid(row=1, column=0)
        self.book_combo = ttk.Combobox(issue_form, values=[b[1] for b in db.view_books()], width=30)
        self.book_combo.grid(row=1, column=1)

        ttk.Label(issue_form, text="Return Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.return_date = ttk.Entry(issue_form, width=30)
        self.return_date.grid(row=2, column=1)

        ttk.Button(issue_form, text="Issue Book", command=self.issue_book).grid(row=3, column=0, pady=10)
        ttk.Button(issue_form, text="View Issued", command=self.view_issued_books).grid(row=3, column=1)

        self.issued_listbox = tk.Listbox(issue_tab, font=("Courier New", 10), height=10, width=90)
        self.issued_listbox.pack(padx=10, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()
        if title and quantity.isdigit():
            db.insert_book(title, author, isbn, int(quantity))
            messagebox.showinfo("Success", "Book added.")
            self.view_books()
        else:
            messagebox.showerror("Error", "Invalid input.")

    def view_books(self):
        self.books_listbox.delete(0, tk.END)
        self.books_listbox.insert(tk.END, f"{'S.No.':<6} {'Title':<25} {'Author':<20} {'ISBN':<15} {'Qty':<5}")
        self.books_listbox.insert(tk.END, "-" * 80)
        for i, row in enumerate(db.view_books(), start=1):
            id, title, author, isbn, quantity = row
            self.books_listbox.insert(tk.END, f"{i:<6} {title:<25} {author:<20} {isbn:<15} {quantity:<5}")

    def register_student(self):
        name = self.student_name.get()
        roll = self.student_roll.get()
        course = self.student_course.get()
        if name and roll:
            try:
                db.insert_student(name, roll, course)
                messagebox.showinfo("Success", "Student registered!")
                self.view_students()
                self.roll_combo['values'] = db.get_student_rolls()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Fill all fields.")

    def view_students(self):
        self.students_listbox.delete(0, tk.END)
        self.students_listbox.insert(tk.END, f"{'S.No.':<6} {'Name':<20} {'Roll':<15} {'Course':<15}")
        self.students_listbox.insert(tk.END, "-" * 60)
        for i, s in enumerate(db.view_students(), start=1):
            id, name, roll, course = s
            self.students_listbox.insert(tk.END, f"{i:<6} {name:<20} {roll:<15} {course:<15}")

    def issue_book(self):
        student_roll = self.roll_combo.get()
        title = self.book_combo.get()
        return_date = self.return_date.get()
        book = db.get_book_by_title(title)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return
        if book[4] <= 0:
            messagebox.showwarning("Stock", "Out of stock.")
            return
        book_id = book[0]
        issue_date = datetime.now().strftime("%Y-%m-%d")
        try:
            db.issue_book(student_roll, book_id, issue_date, return_date)
            messagebox.showinfo("Issued", "Book issued.")
            self.view_issued_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_issued_books(self):
        self.issued_listbox.delete(0, tk.END)
        self.issued_listbox.insert(tk.END, f"{'ID':<4} {'Name':<20} {'Roll':<10} {'Book':<25} {'Issue Date':<12} {'Return':<12}")
        self.issued_listbox.insert(tk.END, "-" * 90)
        for row in db.view_issued_books():
            issue_id, name, roll, title, issue_date, return_date = row
            self.issued_listbox.insert(tk.END, f"{issue_id:<4} {name:<20} {roll:<10} {title:<25} {issue_date:<12} {return_date:<12}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
