[Read me (TAR UMT Student Assistant App).txt](https://github.com/user-attachments/files/22398910/Read.me.TAR.UMT.Student.Assistant.App.txt)# Python
SDF
[Uploading Read me (TAR UMT S# TAR UMT Student Assistant App

## Overview
The **TAR UMT Student Assistant App** is a Python-based desktop application built with Tkinter.  
It serves as a campus companion tool that combines multiple student utilities into a single app, including:

- 🔐 **Login & User Authentication**
- 📊 **GPA Calculator**
- ⏰ **Simple Reminder App**
- 🏢 **Discussion Room Booking System**
- ⚙ **Settings & Password Management**

---

## Features
### 1. Login & Authentication
- Fixed credentials (default: `dft@gmail.com` / `123456`).  
- Email format validation.  
- Error prompts for invalid email or wrong password.  
- Successful login grants access to all features.  
- Logout button replaces login after sign-in.  

### 2. GPA Calculator
- Opens a dedicated window with a GPA calculation tab.  
- Allows students to compute and manage their GPA.  

### 3. Simple Reminder
- Opens a separate Reminder window.  
- Users can create, view, and manage reminders.  
- Data is stored in JSON format.  

### 4. Discussion Room Booking
- Opens the booking system (integrated from `BookingRoom/booking_system.py`).  
- Students can:
  - Choose number of participants (2–8).  
  - Filter rooms by equipment.  
  - Select date/time slots.  
  - Check availability and make/cancel bookings.  
  - View booking details.  

### 5. Settings & Password Reset
- User can reset password by providing:
  - Current password.  
  - New password.  
  - Confirm new password.  
- Validations:
  - Must enter all fields.  
  - Current password must match stored password.  
  - New password must be at least 6 characters.  
  - New and confirm password must match.  
  - New password must differ from old one.  
- Success message shown when password reset completes.  

---

## Requirements
- **Python 3.8+**  
- Tkinter (included in most Python installations)  

If Tkinter is missing:  
- Ubuntu/Debian: `sudo apt install python3-tk`  
- macOS: included with Python.org installer  
- Windows: included with standard Python installer  

---

##Usage Guide

Press Login in the header.
Enter email & password (default: dft@gmail.com / 123456).
Once logged in:

Open GPA Calculator → calculate GPA.

Open Reminder App → manage reminders.

Open Booking System → reserve discussion rooms.

Open Settings → reset password.

4. To log out, press the Logout button.

---

##Error Handling

Invalid email format → "Please enter a valid email address".
Wrong email/password → "Invalid email or password".
Reset password errors:
Empty fields.
Current password incorrect.
New passwords don’t match.
Password too short (< 6).
New password same as old.

=============================================================================
Discussion Room Booking System — README

##Short description

A Tkinter-based desktop application for booking university discussion rooms. Users can filter rooms by capacity and equipment, pick date/time slots, view availability, make bookings, view booking details, and cancel bookings. Data is persisted to JSON files in a local application data folder.

---

##Table of contents

1.Features
2.Requirements
3.Installation & Setup (step-by-step)
4.Configuration notes
5.Run the application
6.Quick usage guide (UI steps)
7.Files & Data storage
8.Sample JSON schema
9.Testing / Basic checks
10.Troubleshooting
11.Developer notes / Extensibility
12.License & attribution

---

##Features

Filter rooms by number of participants and required equipment.
Select date (manual entry or calendar pop-up) and start / end times (30-minute slots between 08:00–20:00).
Validate bookings (no past dates/times, start < end, max duration 2 hours, no overlaps).
Check availability or view all available / booked 30-min slots for a room/date.
View current bookings in a right-hand list with details (room, date, time, purpose, student ID).
Cancel bookings; calendar and lists update immediately.
Data persisted to local JSON files so bookings survive restart.

##Requirements

Python 3.8+ (recommended). The code also works with Python 3.7 in most cases, but 3.8+ is preferred.
Tkinter GUI toolkit (bundled with standard CPython on many platforms).
Standard Python libraries only: tkinter, ttk, scrolledtext, datetime, json, os, calendar. No external pip packages required.

##Platform notes:

Windows: Tkinter is included with the standard Python installer.
Linux (Debian/Ubuntu): you may need to install tk via sudo apt install python3-tk.
macOS: use Python from python.org or ensure Tk is available. Homebrew python may need additional steps to include tk support.

##Installation & Setup (step-by-step)

1. Clone or copy the project

# example using git
git clone <your-repo-url>
cd <repo-folder>

If the code file is BookingRoom/booking_system.py, you can either:

Run it directly from the BookingRoom folder; or
Integrate it into your application launcher (e.g. main_app.py).

2. (Optional) Create a virtual environment
Windows:
python -m venv venv
.\venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

No packages to pip install are required for the current code.

3. Verify Tkinter is working
Run:
python -c "import tkinter; print('tkinter OK, version', tkinter.TkVersion)"

If that prints a version number, Tkinter is available.

4. (Optional) Ensure write permission to your user profile
By default, the app stores data under a folder named BookingAppData inside the user profile directory (Windows USERPROFILE). Make sure your user account can create files there. See Configuration notes if you prefer a different location.

##Configuration notes

Application data folder (default in code):

app_data_dir = os.path.join(os.environ['USERPROFILE'], 'BookingAppData')

On non-Windows systems or to avoid USERPROFILE lookups, change to:

app_data_dir = os.path.join(os.environ.get('USERPROFILE') or os.environ.get('HOME'), 'BookingAppData')

To use the project directory instead, set:

app_data_dir = os.path.join(os.getcwd(), 'BookingAppData')

Time range & intervals: current code uses 08:00–20:00 and 30-minute slots. Modify update_time_slots() or view_available_slots() to change these.
Max booking duration: currently 2 hours (enforced in validate_booking_time()).

---

##Run the application

From the directory where booking_system.py is located:

Windows / macOS / Linux:
python booking_system.py

Or run via your IDE (open file and Run).
If integrating into main_app.py, run that launcher instead.

##Quick usage guide (UI steps)

Select number of participants (spinbox). Minimum 2 (or 2 default), maximum configurable (code currently 2–15 in the revised file).
(Optional) Choose required equipment (radio buttons) — the room list will auto-filter.
Pick a room from the drop-down. Room details appear below.
Choose date: type YYYY-MM-DD or click the calendar icon and select a date. (Past dates disabled.)
Select start & end times (30-minute increments). The UI pre-selects default start/end and blocks past times for today.
Enter purpose and Student ID (required).
Click Check Availability to verify the slot, or click View Available Slots to see all slots on that date and room.
If available, click Book Room to create the booking. You will receive a success message and booking will appear in the right-hand list.
To view details of a booking, select it in the right-hand list and click View Details.
To cancel, select a booking and click Cancel Booking, confirm in the dialog — the booking will be removed and calendar counts will update.

---

##Files & Data storage

On first run, a directory BookingAppData (by default) will be created in your user profile. It contains:

bookings.json — list of bookings (auto-created when a booking is saved).
rooms.json — room definitions (created with default rooms on first run if missing).

You can change the storage path in the code by editing the app_data_dir assignment (see Configuration notes).

---

##Sample JSON schema

bookings.json (example entry)
[
    {
        "id": 1,
        "room": "Medium Conference Room",
        "date": "2025-09-20",
        "start_time": "10:00",
        "end_time": "12:00",
        "purpose": "Group Presentation Practice",
        "participants": 6,
        "student_id": "S1234567",
        "created_at": "2025-09-10 14:35:12"
    }
]

---

##Testing / Basic checks

Confirm Tkinter import: python -c "import tkinter; print(tkinter.TkVersion)".
Manual test cases to try:
Try booking a slot in the past → expect error.
Try booking > 2 hours → expect error.
Book a slot → attempt to book overlapping slot → expect “not available” error.
Cancel a booking → check calendar / right list updates.
For automated testing you can write unit tests that import methods like is_room_available() and validate_booking_time() with mocked data.

---

##Troubleshooting

"No module named tkinter" — install tkinter:
Debian/Ubuntu: sudo apt install python3-tk
macOS: use official Python installer from python.org that bundles Tk; or install ActiveTcl if necessary.
Permission errors writing files — check BookingAppData location and file permissions. Try changing app_data_dir to a writable path (e.g., current project folder).
Calendar does not highlight today or times missing — confirm your system date/time and timezone settings.
GUI looks different across OS — ttk styling differs by platform; the behavior is still functional.

---

##Developer notes / Extensibility

Authentication integration: The system accepts optional current_user to display who booked. Integrate with your Login module to restrict booking features to logged-in users.
External calendar sync: Add iCal/Google Calendar export or API sync as future work.
Database migration: Replace JSON files with SQLite/Postgres for multi-user, concurrent access.
Unit tests: Add a tests/ folder and write tests for is_room_available(), validate_booking_time(), and view_available_slots() logic.
Localization: Date/time formats are fixed to YYYY-MM-DD and %H:%M — add localization if needed.

Example: to change storage to cross-platform:
app_data_dir = os.path.join(os.environ.get('USERPROFILE') or os.environ.get('HOME'), 'BookingAppData')

---

##License & attribution

This code and README may be used and adapted for academic or personal projects. If you will redistribute it or use it for production, consider adding a proper license (e.g., MIT) and acknowledgements.

=============================================================================
Simple Reminder App

A lightweight reminder application built with Python and Tkinter.
This app lets you schedule tasks, receive notifications with sound alerts, snooze reminders, and keep track of completed tasks.


1.Features

   -Add reminders with title, date, time, category, snooze delay, and repeat        option

   -Popup notification with sound alert when it’s time

   -Snooze reminders for later (configurable delay)

   -Mark reminders as done (auto-logs to history)

   -Repeat daily reminders

   -View snoozed reminders separately

   -Import & Export reminders in JSON format

   -Scrollable list with status highlights

      White = Active reminder

      Yellow = Snoozed reminder

      Green = Completed reminder



Project Structure:

ReminderApp/
│── reminder_app.py      # Main application code
│── reminders.json       # Saved reminders (auto-created)
│── history.json         # Completed reminders history (auto-created)
│── README.md            # Project documentation



Requirements:

Python 3.8 or higher

 -Runs on Windows, macOS, Linux

 -Uses built-in modules:

 -tkinter

 -datetime

 -json, os

 -threading, winsound



How to Run

1.Clone or download the project.

2.Run the app:

    python reminder_app.py
3.Add new reminders from the Add New Reminder section.

4.When time is up, a popup appears with options:

    -Done → marks as completed (saved in history)

    -Remind Later → snoozes for X minutes

Data Handling:

  -All reminders are saved to reminders.json automatically.

  -Completed tasks are logged in history.json.

  -Import/Export feature lets you back up or restore reminders.


Next Improvements:

  -Cross-platform sound notifications

  -Search & filter reminders

  -Weekly / monthly repeat options

  -Dark mode theme

License:

  -MIT License © 2025

=============================================================================
Setup Instructions
Ensure Python 3.x is installed on your system

Download all three Python files:

1.gpa_calculator_main.py

2.gpa_chart.py

3.gpa_history.py

Place all files in the same directory

Required Libraries
Python standard libraries only (no additional installations needed)

Tkinter (usually included with Python installations)

Execution Instructions
Run the application by executing the main file:python gpa_calculator_main.py

How to Use
Enter course details (name, credit hours, grade)

1.Click "Add Course" to add to your list

2.Click "Calculate GPA" to compute your GPA

3.Use "Save to History" to store your calculation

4.Use "View History" to review past calculations

5.Use "View Performance Chart" to see a visual representation

Features
Add/remove courses with credit hours and grades

Calculate cumulative GPA

Save and load calculation history

Visualize performance with bar charts

User-friendly graphical interface

tudent Assistant App).txt…]()
