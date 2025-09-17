import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import json
import os
import calendar

class BookingSystem:
    def __init__(self, root, current_user=None):
        self.root = root
        self.current_user = current_user
        self.root.title("Professional Discussion Room Booking System")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f0f2f5')

        # ---------------------- Data Files ----------------------
        app_data_dir = os.path.join(os.environ['USERPROFILE'], 'BookingAppData')
        os.makedirs(app_data_dir, exist_ok=True)
        self.bookings_file = os.path.join(app_data_dir, "bookings.json")
        self.rooms_file = os.path.join(app_data_dir, "rooms.json")
        # --------------------------------------------------------

        # Load data
        self.load_data()

        # Setup UI
        self.setup_ui()

        # Refresh views
        self.refresh_rooms_list()
        self.refresh_bookings_list()

    # ---------------------- Data Management ----------------------
    def load_data(self):
        if os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'r') as f:
                self.bookings = json.load(f)
        else:
            self.bookings = []

        if os.path.exists(self.rooms_file):
            with open(self.rooms_file, 'r') as f:
                self.rooms = json.load(f)
        else:
            # Default rooms
            self.rooms = [
                {"id": 1, "name": "A mall Meeting Room", "capacity": 4, "equipment": ["Monitor", "Whiteboard"]},
                {"id": 2, "name": "Medium Conference Room", "capacity": 8, "equipment": ["Projector", "Whiteboard", "TV"]},
                {"id": 3, "name": "Large Conference Room", "capacity": 12, "equipment": ["Projector", "Video Conferencing", "Smart Board", "Sound System"]},
                {"id": 4, "name": "Executive Boardroom", "capacity": 6, "equipment": [ "Premium Sound", "Video Conferencing", "Smart Table"]},
                {"id": 5, "name": "Training Room", "capacity": 15, "equipment": ["Projector", "Whiteboard", "Sound System", "Multiple Monitors"]}
            ]
            self.save_rooms()

    def save_bookings(self):
        with open(self.bookings_file, 'w') as f:
            json.dump(self.bookings, f, indent=4)

    def save_rooms(self):
        with open(self.rooms_file, 'w') as f:
            json.dump(self.rooms, f, indent=4)

    # ---------------------- UI Setup ----------------------
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure main grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # left
        main_frame.columnconfigure(1, weight=2)  # middle
        main_frame.columnconfigure(2, weight=2)  # right
        main_frame.rowconfigure(1, weight=1)

        # Title frame
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        title_label = tk.Label(title_frame, text="Discussion Room Booking System",
                               font=("Arial", 18, "bold"), fg="white", bg="#3498db")
        title_label.pack(fill=tk.X, pady=10)

        # -------------------- Left Panel --------------------
        left_frame = ttk.LabelFrame(main_frame, text="Room Information & Booking", padding="10")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_frame.columnconfigure(1, weight=1)

        # Number of participants
        ttk.Label(left_frame, text="Number of Participants (2-8):").grid(row=0, column=0, sticky="w", pady=5)
        self.participants_var = tk.IntVar(value=2)
        participants_spin = ttk.Spinbox(left_frame, from_=2, to=8, textvariable=self.participants_var, width=5,
                                        command=self.filter_rooms_by_capacity)
        participants_spin.grid(row=0, column=1, sticky="w", pady=5)

        # Equipment selection
        ttk.Label(left_frame, text="Required Equipment:").grid(row=1, column=0, sticky="w", pady=5)
        self.equipment_var = tk.StringVar(value="")
        equipment_frame = ttk.Frame(left_frame)
        equipment_frame.grid(row=1, column=1, sticky="ew", pady=5)
        all_equipment = set(eq for room in self.rooms for eq in room['equipment'])
        for i, eq in enumerate(sorted(all_equipment)):
            rb = ttk.Radiobutton(equipment_frame, text=eq, value=eq, variable=self.equipment_var,
                                 command=self.filter_rooms_by_equipment)
            rb.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 10))

        # Room selection
        ttk.Label(left_frame, text="Available Rooms:").grid(row=2, column=0, sticky="w", pady=5)
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(left_frame, textvariable=self.room_var, state="readonly")
        self.room_combo.grid(row=2, column=1, sticky="ew", pady=5)
        self.room_combo.bind('<<ComboboxSelected>>', self.on_room_select)

        # Room details
        ttk.Label(left_frame, text="Room Details:").grid(row=3, column=0, sticky="nw", pady=5)
        self.room_details = scrolledtext.ScrolledText(left_frame, width=35, height=6, state=tk.DISABLED)
        self.room_details.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        # Date selection
        ttk.Label(left_frame, text="Booking Date:").grid(row=5, column=0, sticky="w", pady=5)
        date_frame = ttk.Frame(left_frame)
        date_frame.grid(row=5, column=1, sticky="ew", pady=5)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Button(date_frame, text="📅", width=3, command=self.show_date_picker).pack(side=tk.LEFT)

        # Time selection
        ttk.Label(left_frame, text="Start Time:").grid(row=6, column=0, sticky="w", pady=5)
        self.start_time_var = tk.StringVar()
        self.start_time_combo = ttk.Combobox(left_frame, textvariable=self.start_time_var, state="readonly")
        self.start_time_combo.grid(row=6, column=1, sticky="ew", pady=5)
        ttk.Label(left_frame, text="End Time:").grid(row=7, column=0, sticky="w", pady=5)
        self.end_time_var = tk.StringVar()
        self.end_time_combo = ttk.Combobox(left_frame, textvariable=self.end_time_var, state="readonly")
        self.end_time_combo.grid(row=7, column=1, sticky="ew", pady=5)

        # Purpose & Student ID
        ttk.Label(left_frame, text="Purpose:").grid(row=8, column=0, sticky="w", pady=5)
        self.purpose_entry = ttk.Entry(left_frame)
        self.purpose_entry.grid(row=8, column=1, sticky="ew", pady=5)
        ttk.Label(left_frame, text="Student ID:").grid(row=9, column=0, sticky="w", pady=5)
        self.student_id_entry = ttk.Entry(left_frame)
        self.student_id_entry.grid(row=9, column=1, sticky="ew", pady=5)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="Check Availability", command=self.check_availability).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Book Room", command=self.book_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Available Slots", command=self.view_available_slots).pack(side=tk.LEFT, padx=5)

        # -------------------- Middle Panel --------------------
        middle_frame = ttk.LabelFrame(main_frame, text="Calendar View", padding="5")
        middle_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 5))
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # Calendar navigation
        nav_frame = ttk.Frame(middle_frame)
        nav_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Button(nav_frame, text="◀", width=3, command=lambda: self.change_month(-1)).pack(side=tk.LEFT)
        self.month_year_var = tk.StringVar()
        month_label = ttk.Label(nav_frame, textvariable=self.month_year_var, font=("Arial", 12, "bold"))
        month_label.pack(side=tk.LEFT, expand=True)
        ttk.Button(nav_frame, text="▶", width=3, command=lambda: self.change_month(1)).pack(side=tk.LEFT, padx=(0, 5))

        self.cal_frame = ttk.Frame(middle_frame)
        self.cal_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # -------------------- Right Panel --------------------
        right_frame = ttk.LabelFrame(main_frame, text="Current Bookings", padding="10")
        right_frame.grid(row=1, column=2, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        columns = ('room', 'date', 'time', 'purpose', 'student_id')
        self.bookings_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        for col, width in zip(columns, [125, 65, 65, 100, 80]):
            self.bookings_tree.heading(col, text=col.capitalize())
            self.bookings_tree.column(col, width=width)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscroll=scrollbar.set)
        self.bookings_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        actions_frame = ttk.Frame(right_frame)
        actions_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(actions_frame, text="View Details", command=self.view_booking_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Cancel Booking", command=self.cancel_booking).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Refresh", command=self.refresh_bookings_list).pack(side=tk.LEFT, padx=5)

        # Initialize calendar & time slots
        self.current_date = datetime.now()
        self.update_calendar()
        self.update_time_slots()


    def configure_calendar_grid(self):
            """Ensure uniform cell sizing in calendar"""
            # Set uniform column and row weights
            for col in range(7):
                self.cal_frame.columnconfigure(col, weight=1, uniform="calendar_col")
            for row in range(7):  # 6 weeks + header
                self.cal_frame.rowconfigure(row, weight=1, uniform="calendar_row")
    
    def configure_styles(self):
        style = ttk.Style()
        
        # Configure styles for different elements
        style.configure("Title.TFrame", background="#3498db")
        style.configure("Card.TLabelframe", borderwidth=2, relief="raised")
        
        # Button styles
        style.configure("Primary.TButton", foreground="white", background="#3498db")
        style.map("Primary.TButton", background=[('active', '#2980b9')])
        
        style.configure("Success.TButton", foreground="white", background="#27ae60")
        style.map("Success.TButton", background=[('active', '#229954')])
        
        style.configure("Info.TButton", foreground="white", background="#17a2b8")
        style.map("Info.TButton", background=[('active', '#138496')])
        
        style.configure("Danger.TButton", foreground="white", background="#dc3545")
        style.map("Danger.TButton", background=[('active', '#c82333')])
    
    def filter_rooms_by_capacity(self):
        participants = self.participants_var.get()
        filtered_rooms = [room for room in self.rooms if room['capacity'] >= participants]
        self.update_room_combo(filtered_rooms)
    
    def filter_rooms_by_equipment(self):
        selected_equipment = self.equipment_var.get()
        participants = self.participants_var.get()

        filtered_rooms = []
        for room in self.rooms:
            if room['capacity'] >= participants:
                if selected_equipment == "" or selected_equipment in room['equipment']:
                    filtered_rooms.append(room)

        self.update_room_combo(filtered_rooms)

    
    def update_room_combo(self, rooms):
        rooms_list = [room['name'] for room in rooms]
        self.room_combo['values'] = rooms_list

        if rooms_list:
            # If the currently selected room is in the new list, keep it
            if self.room_var.get() in rooms_list:
                self.on_room_select()
            else:
                # Otherwise, select the first room in the filtered list
                self.room_combo.current(0)
                self.on_room_select()
        else:
            # Keep dropdown empty
            self.room_combo.set('')
            self.room_combo['values'] = []

            # Show message in right panel
            self.room_details.config(state=tk.NORMAL)
            self.room_details.delete("1.0", tk.END)
            self.room_details.insert(tk.END, "❌ No rooms that match your requirements.")
            self.room_details.config(state=tk.DISABLED)
    
    def refresh_rooms_list(self):
        self.filter_rooms_by_capacity()
    
    def on_room_select(self, event=None):
        room_name = self.room_var.get()
        room = next((r for r in self.rooms if r['name'] == room_name), None)
        
        if room:
            details = f"🏢 Room: {room['name']}\n"
            details += f"👥 Capacity: {room['capacity']} people\n"
            details += f"⏰ Max Booking: 2 hours\n\n"
            details += f"🛠 Equipment:\n"
            for item in room['equipment']:
                details += f"   • {item}\n"
            
            self.room_details.config(state=tk.NORMAL)
            self.room_details.delete(1.0, tk.END)
            self.room_details.insert(tk.END, details)
            self.room_details.config(state=tk.DISABLED)
    
    def show_date_picker(self):
        def on_date_select():
            selected_date = cal.get_date()
            self.date_var.set(selected_date.strftime("%Y-%m-%d"))
            self.update_time_slots()
            top.destroy()
        
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.geometry("500x500")
        top.transient(self.root)
        top.grab_set()
        
        # Get current date
        current_date = datetime.now()
        if self.date_var.get():
            try:
                current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            except:
                pass
        
        # Create calendar
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(current_date.year, current_date.month)
        
        # Calendar header
        header = ttk.Label(top, text=current_date.strftime("%B %Y"), font=("Arial", 12, "bold"))
        header.pack(pady=10)
        
        # Days frame
        days_frame = ttk.Frame(top)
        days_frame.pack(padx=10, pady=5)
        
        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ttk.Label(days_frame, text=day, width=4, font=("Arial", 8, "bold")).grid(row=0, column=i)
        
        # Create days buttons
        today = datetime.now().date()
        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day != 0:
                    day_date = datetime(current_date.year, current_date.month, day).date()
                    btn = ttk.Button(days_frame, text=str(day), width=4,
                                   command=lambda d=day_date: self.date_var.set(d.strftime("%Y-%m-%d")) or top.destroy() or self.update_time_slots())
                    
                    if day_date < today:
                        btn.state(['disabled'])  # Disable past dates
                    elif day_date == today:
                        btn.configure(style="Success.TButton")  # Highlight today
                    
                    btn.grid(row=week_idx+1, column=day_idx, padx=2, pady=2)
        
        ttk.Button(top, text="Cancel", command=top.destroy).pack(pady=10)
    
    def update_time_slots(self):
        if not self.date_var.get():
            return
        
        try:
            selected_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date()
            today = datetime.now().date()
            current_time = datetime.now().time()
            
            # Generate time slots
            time_slots = []
            for hour in range(8, 20):  # 8 AM to 8 PM
                for minute in [0, 30]:  # Every 30 minutes
                    time_str = f"{hour:02d}:{minute:02d}"
                    
                    # If selected date is today, disable past times
                    if selected_date == today:
                        slot_time = datetime.strptime(time_str, "%H:%M").time()
                        if slot_time < current_time:
                            continue  # Skip past times for today
                    
                    time_slots.append(time_str)
            
            self.start_time_combo['values'] = time_slots
            self.end_time_combo['values'] = time_slots
            
            if time_slots:
                self.start_time_combo.set(time_slots[0])
                # Set end time to 2 hours later (maximum allowed)
                start_index = time_slots.index(time_slots[0])
                end_index = min(start_index + 4, len(time_slots) - 1)  # 4 slots = 2 hours
                self.end_time_combo.set(time_slots[end_index])
                
        except ValueError:
            pass
    
    def validate_booking_time(self):
        try:
            selected_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date()
            today = datetime.now().date()
            
            # Check if date is in the past
            if selected_date < today:
                messagebox.showerror("Error", "Cannot book rooms for past dates!")
                return False
            
            start_time = datetime.strptime(self.start_time_var.get(), "%H:%M").time()
            end_time = datetime.strptime(self.end_time_var.get(), "%H:%M").time()
            
            # Check if start and end times are the same
            if start_time == end_time:
                messagebox.showerror("Error", "Start time and end time cannot be the same!")
                return False
            
            # Check if end time is after start time
            if end_time <= start_time:
                messagebox.showerror("Error", "End time must be after start time!")
                return False
            
            # Check maximum booking duration (2 hours)
            start_dt = datetime.combine(selected_date, start_time)
            end_dt = datetime.combine(selected_date, end_time)
            duration = (end_dt - start_dt).total_seconds() / 3600  # hours
            
            if duration > 2:
                messagebox.showerror("Error", "Maximum booking duration is 2 hours!")
                return False
            
            # If booking for today, check if time is in the future
            if selected_date == today:
                current_time = datetime.now().time()
                if start_time < current_time:
                    messagebox.showerror("Error", "Cannot book rooms for past times!")
                    return False
            
            return True
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format!")
            return False
    
    def check_availability(self):
        if not self.validate_booking_time():
            return
        
        room_name = self.room_var.get()
        date = self.date_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        
        if not all([room_name, date, start_time, end_time]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        # Check if the room is available
        is_available = self.is_room_available(room_name, date, start_time, end_time)
        
        if is_available:
            messagebox.showinfo("Availability", f"✅ {room_name} is available on {date} from {start_time} to {end_time}")
        else:
            messagebox.showwarning("Availability", f"❌ {room_name} is not available on {date} from {start_time} to {end_time}")
    
    def is_room_available(self, room_name, date, start_time, end_time):
        # Convert to datetime objects for comparison
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
        
        for booking in self.bookings:
            if booking['room'] == room_name and booking['date'] == date:
                # Check for time overlap
                booking_start = datetime.strptime(f"{date} {booking['start_time']}", "%Y-%m-%d %H:%M")
                booking_end = datetime.strptime(f"{date} {booking['end_time']}", "%Y-%m-%d %H:%M")
                
                if (start_dt < booking_end and end_dt > booking_start):
                    return False
        
        return True
    
    def book_room(self):
        if not self.validate_booking_time():
            return
        
        room_name = self.room_var.get()
        date = self.date_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        purpose = self.purpose_entry.get()
        student_id = self.student_id_entry.get().strip()
        
        if not all([room_name, date, start_time, end_time, purpose, student_id]):
            messagebox.showerror("Error", "Please fill all required fields including Student ID")
            return
        
        # Check availability
        if not self.is_room_available(room_name, date, start_time, end_time):
            messagebox.showerror("Error", "The room is not available at the selected time")
            return
        
        # Create booking
        booking_id = len(self.bookings) + 1
        booking = {
            "id": booking_id,
            "room": room_name,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "purpose": purpose,
            "participants": self.participants_var.get(),
            "student_id": student_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.bookings.append(booking)
        self.save_bookings()
        self.refresh_bookings_list()  # This will now also refresh the calendar
        
        messagebox.showinfo("Success", f"✅ Room booked successfully!\nBooking ID: {booking_id}\n{room_name} on {date} from {start_time} to {end_time}")
        
        # Clear form
        self.purpose_entry.delete(0, tk.END)
        self.student_id_entry.delete(0, tk.END)

    def view_available_slots(self):
        room_name = self.room_var.get()
        date = self.date_var.get().strip()

        if not room_name:
            messagebox.showwarning("Input Error", "Please select a room first.")
            return
            
        if not date:
            messagebox.showwarning("Input Error", "Please select a date first.")
            return

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD format.")
            return

        # Get all bookings for this room on this date
        room_bookings = [b for b in self.bookings if b["room"] == room_name and b["date"] == date]
        
        # Define all possible time slots (08:00–20:00, 30-min intervals)
        all_slots = []
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("20:00", "%H:%M")
        
        current = start_time
        while current < end_time:
            slot_end = current + timedelta(minutes=30)
            all_slots.append((
                current.strftime("%H:%M"),
                slot_end.strftime("%H:%M")
            ))
            current = slot_end

        # Convert booked times to 30-minute slots and store booking details
        booked_slots = []
        booking_info = {}  # Store booking information for each slot
        
        for booking in room_bookings:
            try:
                booking_start = datetime.strptime(booking["start_time"], "%H:%M")
                booking_end = datetime.strptime(booking["end_time"], "%H:%M")
                
                # Break down the booking into 30-minute intervals
                current_slot = booking_start
                while current_slot < booking_end:
                    slot_end = current_slot + timedelta(minutes=30)
                    slot_key = (current_slot.strftime("%H:%M"), slot_end.strftime("%H:%M"))
                    booked_slots.append(slot_key)
                    
                    # Store booking information
                    booking_info[slot_key] = {
                        'purpose': booking['purpose'],
                        'participants': booking.get('participants', 'N/A')
                    }
                    current_slot = slot_end
            except ValueError:
                continue  # Skip invalid time formats

        # Find available and booked slots
        available_slots = []
        booked_slots_detailed = []
        
        for slot in all_slots:
            slot_str = f"{slot[0]} - {slot[1]}"
            if slot in booked_slots:
                # This slot is booked, get booking details
                details = booking_info.get(slot, {})
                purpose = details.get('purpose', 'Unknown purpose')
                booked_slots_detailed.append(f"{slot_str} (Booked: {purpose})")
            else:
                available_slots.append(slot_str)

        # Create a new window to display both available and booked slots
        slot_window = tk.Toplevel(self.root)
        slot_window.title(f"Time Slot Availability - {room_name} on {date}")
        slot_window.geometry("600x500")
        
        # Header
        header_frame = ttk.Frame(slot_window)
        header_frame.pack(pady=10)
        
        ttk.Label(header_frame, text=f"Time Slot Availability for:", 
                font=("Arial", 12, "bold")).pack()
        ttk.Label(header_frame, text=f"{room_name} on {date}", 
                font=("Arial", 10, "bold")).pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(slot_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Available Slots Tab - Only show truly available slots
        available_frame = ttk.Frame(notebook)
        notebook.add(available_frame, text=f"Available Slots ({len(available_slots)})")
        
        if available_slots:
            available_text = scrolledtext.ScrolledText(available_frame, width=70, height=15, font=("Arial", 9))
            available_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            available_text.insert(tk.END, f"✅ AVAILABLE TIME SLOTS ({len(available_slots)}):\n\n")
            for i, slot in enumerate(available_slots, 1):
                available_text.insert(tk.END, f"{i:2d}. {slot}\n")
            
            available_text.config(state=tk.DISABLED)
        else:
            ttk.Label(available_frame, text="❌ No available time slots - all slots are booked", 
                    font=("Arial", 10), foreground="red").pack(pady=50)
        
        # Booked Slots Tab
        booked_frame = ttk.Frame(notebook)
        notebook.add(booked_frame, text=f"Booked Slots ({len(booked_slots_detailed)})")
        
        if booked_slots_detailed:
            booked_text = scrolledtext.ScrolledText(booked_frame, width=70, height=15, font=("Arial", 9))
            booked_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            booked_text.insert(tk.END, f"📅 BOOKED TIME SLOTS ({len(booked_slots_detailed)}):\n\n")
            for i, slot_info in enumerate(booked_slots_detailed, 1):
                booked_text.insert(tk.END, f"{i:2d}. {slot_info}\n")
            
            booked_text.config(state=tk.DISABLED)
        else:
            ttk.Label(booked_frame, text="✅ No bookings for this room and date", 
                    font=("Arial", 10), foreground="green").pack(pady=50)
        
        # Close button
        button_frame = ttk.Frame(slot_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Close", 
                command=slot_window.destroy).pack()
        
    def refresh_bookings_list(self):
        # Clear current items
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        # Add bookings to treeview
        for booking in sorted(self.bookings, key=lambda x: (x['date'], x['start_time'])):
            self.bookings_tree.insert('', tk.END, values=(
                booking['room'],
                booking['date'],
                f"{booking['start_time']} - {booking['end_time']}",
                booking['purpose'],
                booking.get('student_id', 'N/A')
            ))
        
        # Also refresh the calendar view to update booking counts
        self.update_calendar()
    
    def view_booking_details(self):
        selected_item = self.bookings_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to view details")
            return
        
        item = self.bookings_tree.item(selected_item[0])
        room, date, time, purpose, student_id = item['values']  # Added student_id
        
        # Find the complete booking details
        booking = next((b for b in self.bookings if 
                    b['room'] == room and 
                    b['date'] == date and 
                    f"{b['start_time']} - {b['end_time']}" == time), None)
        
        if booking:
            details = f"📋 Booking ID: {booking['id']}\n"
            details += f"🏢 Room: {booking['room']}\n"
            details += f"📅 Date: {booking['date']}\n"
            details += f"⏰ Time: {booking['start_time']} - {booking['end_time']}\n"
            details += f"🎯 Purpose: {booking['purpose']}\n"
            details += f"👥 Participants: {booking.get('participants', 'N/A')}\n"
            details += f"🎓 Student ID: {booking.get('student_id', 'N/A')}\n"  # Added Student ID
            details += f"📅 Booked at: {booking['created_at']}"
            
            messagebox.showinfo("Booking Details", details)
    
    def cancel_booking(self):
        selected_item = self.bookings_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a booking to cancel")
            return
        
        item = self.bookings_tree.item(selected_item[0])
        room, date, time, purpose, student_id = item['values']
        
        # Confirm cancellation
        if messagebox.askyesno("Confirm Cancellation", 
                            f"Are you sure you want to cancel the booking for {room} on {date} at {time}?"):
            # Find and remove the booking
            for i, booking in enumerate(self.bookings):
                if (booking['room'] == room and 
                    booking['date'] == date and 
                    f"{booking['start_time']} - {booking['end_time']}" == time):
                    del self.bookings[i]
                    self.save_bookings()
                    self.refresh_bookings_list()  # This will now also refresh the calendar
                    messagebox.showinfo("Success", "✅ Booking cancelled successfully")
                    return
                
    def refresh_all(self):
        """Refresh both bookings list and calendar"""
        self.refresh_bookings_list()
        self.update_calendar()
    
    def update_calendar(self):
        # Clear previous calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
        
        # Set month and year label
        self.month_year_var.set(self.current_date.strftime("%B %Y"))
        
        # Get calendar for the current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = ttk.Label(self.cal_frame, text=day, font=("Arial", 7, "bold"), 
                            foreground="black", anchor="center")
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Create calendar days with smaller uniform size
        today = datetime.now().date()
        max_weeks = 6  # Maximum number of weeks to display for consistent size
        
        for week_idx in range(max_weeks):
            for day_idx in range(7):
                day_frame = ttk.Frame(self.cal_frame, relief=tk.RAISED, borderwidth=1)
                day_frame.grid(row=week_idx+1, column=day_idx, sticky="nsew", padx=1, pady=1)
                
                # Configure smaller uniform cell size
                day_frame.grid_propagate(False)  # Prevent frame from resizing to content
                day_frame.config(width=30, height=15)  # Reduced from 80x60 to 60x45
                
                if week_idx < len(cal) and day_idx < len(cal[week_idx]):
                    day = cal[week_idx][day_idx]
                    if day != 0:
                        date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                        day_date = datetime(self.current_date.year, self.current_date.month, day).date()
                        
                        # Check if there are bookings on this day
                        booking_count = sum(1 for b in self.bookings if b['date'] == date_str)
                        
                        # Style based on date
                        if day_date == today:
                            day_label = ttk.Label(day_frame, text=str(day), 
                                                font=("Arial", 8, "bold"),  # Smaller font
                                                foreground="white", background="#27ae60",
                                                anchor="center")
                        elif day_date < today:
                            day_label = ttk.Label(day_frame, text=str(day), 
                                                font=("Arial", 8),  # Smaller font
                                                foreground="#95a5a6", anchor="center")
                        else:
                            day_label = ttk.Label(day_frame, text=str(day), 
                                                font=("Arial", 8),  # Smaller font
                                                foreground="black", anchor="center")
                        
                        day_label.place(relx=0.5, rely=0.3, anchor="center")
                        
                        if booking_count > 0:
                            color = "#e74c3c" if booking_count > 2 else "#f39c12" if booking_count > 1 else "#27ae60"
                            booking_label = ttk.Label(day_frame, text=f"📅{booking_count}", 
                                                    foreground=color, font=("Arial", 6),  # Smaller font
                                                    anchor="center")
                            booking_label.place(relx=0.5, rely=0.7, anchor="center")
                    else:
                        # Empty cell for days not in this month
                        empty_label = ttk.Label(day_frame, text="", background="light gray")
                        empty_label.pack(fill=tk.BOTH, expand=True)
                else:
                    # Empty cell for extra weeks
                    empty_label = ttk.Label(day_frame, text="", background="light gray")
                    empty_label.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for uniform cell sizing
        for i in range(7):  # 7 columns
            self.cal_frame.columnconfigure(i, weight=1, uniform="calendar_col")
        for i in range(max_weeks + 1):  # +1 for header row
            self.cal_frame.rowconfigure(i, weight=1, uniform="calendar_row")
    
    def change_month(self, delta):
        # Calculate new month
        month = self.current_date.month + delta
        year = self.current_date.year
        
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        
        self.current_date = self.current_date.replace(year=year, month=month)
        self.update_calendar()

def main():
    root = tk.Tk()
    app = BookingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
