import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# Directory and file paths
DATA_DIR = 'hospital_data'
PATIENT_FILE = os.path.join(DATA_DIR, 'patients.csv')
DOCTOR_FILE = os.path.join(DATA_DIR, 'doctors.csv')
NURSE_FILE = os.path.join(DATA_DIR, 'nurses.csv')
ROOM_FILE = os.path.join(DATA_DIR, 'rooms.csv')
APPOINTMENT_FILE = os.path.join(DATA_DIR, 'appointments.csv')  # New file

os.makedirs(DATA_DIR, exist_ok=True)

# Initialize CSVs with headers
def init_csv(file_path, headers, default_data=None):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            if default_data:
                writer.writerows(default_data)

init_csv(PATIENT_FILE, ['ID', 'Name', 'Age', 'Gender', 'Disease'])
init_csv(DOCTOR_FILE, ['ID', 'Name', 'Specialization', 'Phone'])
init_csv(NURSE_FILE, ['ID', 'Name', 'Shift', 'Phone'])
init_csv(ROOM_FILE, ['Room No', 'Type', 'Status'], [
    ['101', 'ICU', 'Occupied'],
    ['102', 'General', 'Available'],
    ['103', 'Emergency', 'Available'],
    ['104', 'ICU', 'Available'],
    ['105', 'General', 'Occupied'],
])
init_csv(APPOINTMENT_FILE, ['Appointment ID', 'Patient ID', 'Doctor ID', 'Date', 'Time'])  # Initialize appointments

# ---------------- Utility: Center Window ---------------- #
def center_window(win, width, height):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ---------------- Hospital Management Main App ---------------- #
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        center_window(self.root, 800, 600)
        self.root.configure(bg="#e6f2ff")

        title = tk.Label(root, text="🏥 Hospital Management System", font=("Arial", 26, "bold"), bg="#e6f2ff", fg="navy")
        title.pack(pady=15)

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#e6f2ff")
        btn_frame.pack(pady=20)

        options = [
            ("➕ Add Patient", self.add_patient),
            ("➕ Add Doctor", self.add_doctor),
            ("➕ Add Nurse", self.add_nurse),
            ("📋 View Patients", self.view_patients),
            ("📋 View Doctors", self.view_doctors),
            ("📋 View Nurses", self.view_nurses),
            ("🏠 View Available Rooms", self.view_rooms),
            ("📅 Manage Appointments", self.manage_appointments),  # New option
        ]

        for i, (text, command) in enumerate(options):
            btn = tk.Button(btn_frame, text=text, width=25, font=("Arial", 13, "bold"),
                            bg="#b3d9ff", fg="black", relief="raised", command=command)
            btn.grid(row=i // 2, column=i % 2, padx=15, pady=10, sticky="nsew")

    def add_entry(self, fields, file_path, title):
        def submit():
            data = [entry.get() for entry in entries]
            if any(not val for val in data):
                messagebox.showerror("Error", "All fields are required.")
                return
            with open(file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            messagebox.showinfo("Success", f"{title} added successfully.")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title(f"Add {title}")
        center_window(top, 400, 300)

        entries = []
        for idx, field in enumerate(fields):
            tk.Label(top, text=field + ":", font=("Arial", 12)).grid(row=idx, column=0, pady=5, padx=10, sticky='e')
            e = tk.Entry(top, font=("Arial", 12), width=25)
            e.grid(row=idx, column=1, pady=5, padx=10)
            entries.append(e)

        tk.Button(top, text="Submit", command=submit, bg="#66cc66", fg="white",
                  font=("Arial", 12, "bold")).grid(row=len(fields), columnspan=2, pady=15)

    def view_data(self, file_path, title):
        top = tk.Toplevel(self.root)
        top.title(title)
        center_window(top, 600, 400)
        top.configure(bg="#f9f9f9")

        frame = tk.Frame(top)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        tree = ttk.Treeview(frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        tree.pack(expand=True, fill='both')

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            tree["columns"] = headers
            tree["show"] = "headings"
            for header in headers:
                tree.heading(header, text=header)
                tree.column(header, width=150, anchor="center")
            for row in reader:
                tree.insert("", "end", values=row)

        tk.Button(top, text="⬅ Back to Home", bg="orange", fg="black",
                  font=("Arial", 12, "bold"), command=top.destroy).pack(pady=10)

    # ---------------- Appointment Management ---------------- #
    def manage_appointments(self):
        top = tk.Toplevel(self.root)
        top.title("Appointments")
        center_window(top, 600, 400)
        top.configure(bg="#f9f9f9")

        frame = tk.Frame(top)
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        tree_scroll_y = tk.Scrollbar(frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = tk.Scrollbar(frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        tree = ttk.Treeview(frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        tree.pack(expand=True, fill='both')

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        def load_data():
            for i in tree.get_children():
                tree.delete(i)
            with open(APPOINTMENT_FILE, newline='') as f:
                reader = csv.reader(f)
                headers = next(reader)
                tree["columns"] = headers
                tree["show"] = "headings"
                for header in headers:
                    tree.heading(header, text=header)
                    tree.column(header, width=150, anchor="center")
                for row in reader:
                    tree.insert("", "end", values=row)

        def add_appointment():
            def submit():
                data = [entry.get() for entry in entries]
                if any(not val for val in data):
                    messagebox.showerror("Error", "All fields are required.")
                    return
                with open(APPOINTMENT_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                messagebox.showinfo("Success", "Appointment added successfully.")
                load_data()
                top_add.destroy()

            top_add = tk.Toplevel(top)
            top_add.title("Add Appointment")
            center_window(top_add, 400, 350)

            fields = ['Appointment ID', 'Patient ID', 'Doctor ID', 'Date', 'Time']
            entries = []
            for idx, field in enumerate(fields):
                tk.Label(top_add, text=field+":", font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky="e")
                e = tk.Entry(top_add, font=("Arial", 12), width=25)
                e.grid(row=idx, column=1, padx=10, pady=5)
                entries.append(e)

            tk.Button(top_add, text="Submit", command=submit, bg="#66cc66", fg="white",
                      font=("Arial", 12, "bold")).grid(row=len(fields), columnspan=2, pady=15)

        def print_appointment():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Error", "Please select an appointment to print.")
                return
            data = tree.item(selected)['values']
            info = f"""
Appointment Details

Appointment ID: {data[0]}
Patient ID: {data[1]}
Doctor ID: {data[2]}
Date: {data[3]}
Time: {data[4]}
"""
            print_win = tk.Toplevel(top)
            print_win.title("Print Appointment")
            center_window(print_win, 400, 300)
            tk.Label(print_win, text="📄 Appointment Details", font=("Arial", 14, "bold")).pack(pady=10)
            text = tk.Text(print_win, font=("Arial", 12), width=40, height=10)
            text.pack(padx=10, pady=10)
            text.insert("1.0", info)
            text.config(state="disabled")
            tk.Button(print_win, text="Close", command=print_win.destroy,
                      bg="orange", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(top, bg="#f9f9f9")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="➕ Add Appointment", command=add_appointment,
                  bg="#66cc66", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="🖨 Print Appointment", command=print_appointment,
                  bg="#3399ff", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="⬅ Back", command=top.destroy,
                  bg="orange", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)

        load_data()

    # ---------------- Button functions ---------------- #
    def add_patient(self): self.add_entry(['ID', 'Name', 'Age', 'Gender', 'Disease'], PATIENT_FILE, "Patient")
    def add_doctor(self): self.add_entry(['ID', 'Name', 'Specialization', 'Phone'], DOCTOR_FILE, "Doctor")
    def add_nurse(self): self.add_entry(['ID', 'Name', 'Shift', 'Phone'], NURSE_FILE, "Nurse")
    def view_patients(self): self.view_data(PATIENT_FILE, "Patients List")
    def view_doctors(self): self.view_data(DOCTOR_FILE, "Doctors List")
    def view_nurses(self): self.view_data(NURSE_FILE, "Nurses List")
    def view_rooms(self): self.view_data(ROOM_FILE, "Available Rooms")

# ---------------- Login Page ---------------- #
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Hospital Management System")
        center_window(self.root, 400, 250)
        self.root.configure(bg="#f2f2f2")

        tk.Label(root, text="🔐 Login", font=("Arial", 22, "bold"), bg="#f2f2f2", fg="black").pack(pady=10)

        login_frame = tk.Frame(root, bg="#f2f2f2")
        login_frame.pack(pady=10)

        tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), width=20)
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(root, text="Login", font=("Arial", 13, "bold"), bg="#66ccff", fg="black",
                  width=12, command=self.check_login).pack(pady=15)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin123":
            self.root.destroy()
            main_root = tk.Tk()
            HospitalApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

# ---------------- Run the Program ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
