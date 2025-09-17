# Python
# TAR UMT Student Assistant App

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

1.	Press Login in the header.
2.	Enter email & password (default: dft@gmail.com / 123456).
3.	Once logged in:

⦁	Open GPA Calculator → calculate GPA.
⦁	
⦁	Open Reminder App → manage reminders.
⦁	
⦁	Open Booking System → reserve discussion rooms.
⦁	
⦁	Open Settings → reset password.

4. To log out, press the Logout button.

---

##Error Handling

⦁	Invalid email format → "Please enter a valid email address".
⦁	Wrong email/password → "Invalid email or password".
⦁	Reset password errors:
⦁	Empty fields.
⦁	Current password incorrect.
⦁	New passwords don’t match.
⦁	Password too short (< 6).
⦁	New password same as old.




