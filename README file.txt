🏥 Hospital Management System

A simple yet efficient desktop-based Hospital Management System built using Python's Tkinter library for GUI and CSV files for data storage. This project allows users to manage hospital-related operations such as adding/viewing patients, doctors, nurses, rooms, and appointments through an intuitive graphical interface.

📌 Features

✔ User Authentication (Login)
✔ Add & View Patients – Store patient details like ID, Name, Age, Gender, and Disease
✔ Add & View Doctors – Store doctor details like ID, Name, Specialization, and Phone
✔ Add & View Nurses – Store nurse details like ID, Name, Shift, and Phone
✔ View Available Rooms – Room information with type and status
✔ Manage Appointments – Add, view, and print appointment details
✔ Data Persistence using CSV files stored in a hospital_data folder
✔ User-friendly interface with responsive layout and easy navigation

hospital_data/: Folder that stores CSV files with headers and data

hospital_system.py: Main Python script with GUI and functionality

README.md: Project documentation

🚀 Installation and Setup
✅ Prerequisites

Python 3.x installed

Tkinter (usually comes pre-installed with Python)

✅ Steps

Clone or download this repository.

Ensure Python 3 is installed on your system.

Run the program:

python hospital_system.py


Login with the following credentials:

Username: admin

Password: admin123

Use the graphical interface to add/view data and manage appointments.

📦 CSV File Details
1. patients.csv

| ID | Name | Age | Gender | Disease |

2. doctors.csv

| ID | Name | Specialization | Phone |

3. nurses.csv

| ID | Name | Shift | Phone |

4. rooms.csv

| Room No | Type | Status |

5. appointments.csv

| Appointment ID | Patient ID | Doctor ID | Date | Time |

The files are automatically created with headers when you first run the application.

🎨 User Interface

Clean and modern UI with consistent styling

Navigation buttons for different operations

Scrollable tables for data display

Form popups for adding new entries

Print-friendly appointment view

✅ Future Improvements

✔ Data validation and error handling enhancements
✔ Integration with SQLite or other database systems
✔ Report generation and analytics
✔ User role management
✔ Export/Import features in CSV or PDF format