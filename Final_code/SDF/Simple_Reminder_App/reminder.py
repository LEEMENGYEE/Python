import tkinter as tk
from tkinter import ttk, messagebox, filedialog # for GUI
from datetime import datetime, timedelta # for date/time handling
import json
import os
import threading
import winsound

class ReminderApp:
    BG_COLOR = "#f5f7fa"
    CARD_BG = "#ffffff"
    CARD_HOVER = "#e0f0ff"
    DONE_BG = "#d4edda"
    SNOOZED_BG = "#fff3cd"
    PRIMARY_COLOR = "#4a6fa5"
    TEXT_COLOR = "#333333"
    ACCENT_COLOR = "#114E6F"
    FONT_TITLE = ("Segoe UI", 10, "bold")
    FONT_NORMAL = ("Segoe UI", 9)
    FONT_SMALL = ("Segoe UI", 8)

    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Simple Reminder App")
        self.root.geometry("800x800")
        self.root.configure(bg=self.BG_COLOR)

        # use absolute path for data files
        base_dir = os.path.dirname(os.path.abspath(__file__)) # directory of the script
        self.data_file = os.path.join(base_dir, "reminders.json") # file to store reminders
        self.history_file = os.path.join(base_dir, "history.json") # file to store history

        self.reminders = [] # list of reminders
        self.history = []
        self.alarm_thread = None # thread for alarm sound
        self.alarm_active = False 

        self.setup_ui()
        self.load_reminders()
        self.load_history()
        self.update_reminder_list()
        self.check_reminders()
    # ================= Data Handling =================
    def load_reminders(self):
     if os.path.exists(self.data_file):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        except:
            data = []
     else:
        data = []

     self.reminders = [] # reset reminders list
     for r in data:
        # ensure time is a datetime object
        if isinstance(r["time"], str):
            r["time"] = datetime.strptime(r["time"], "%Y-%m-%d %H:%M") # convert string to datetime
        # snooze_until may not exist
        if "snooze_until" in r and isinstance(r["snooze_until"], str):
            try:
                r["snooze_until"] = datetime.strptime(r["snooze_until"], "%Y-%m-%d %H:%M:%S") 
            except:
                r.pop("snooze_until", None)
        r.setdefault("repeat", False) # default to no repeat
        r.setdefault("done", False)
        r.setdefault("snooze_delay", 5) 
        self.reminders.append(r) # add to reminders list


    def save_reminders(self):
    # Create the file if it doesn't exist
     if not os.path.exists(self.data_file): # create empty file
        with open(self.data_file, "w") as f:                # create file
            f.write("[]")  # initialize with empty list

     with open(self.data_file, "w") as f:       # save reminders to file
        json.dump([                                   
            {
                **r,                                            # unpack all fields
                "time": r["time"].strftime("%Y-%m-%d %H:%M"),
                **({"snooze_until": r["snooze_until"].strftime("%Y-%m-%d %H:%M:%S")}  # only if exists and is datetime
                   if isinstance(r.get("snooze_until"), datetime) else {})        # unpack if exists
            } for r in self.reminders
        ], f, indent=2)  # pretty print with indent


    def load_history(self):             # load history from file
        if os.path.exists(self.history_file):  # file exists
            with open(self.history_file, "r") as f:   # read file
                self.history = json.load(f)               # load JSON data
        else:
            self.history = []   # no history file, start fresh


    def save_history(self, record):   # save a new history record
        self.history.append(record) 
        with open(self.history_file, "w") as f:  # write updated history
            json.dump(self.history, f, indent=2) 

    # ================= Alarm =================
    def play_alarm_sound(self): 
        while self.alarm_active:          # loop while alarm is active
            try:
                winsound.Beep(1000, 500) # frequency, duration 
            except:
                pass                     # ignore sound errors

    # ================= Check Reminders =================
    def check_reminders(self):               
        now = datetime.now()              # current time
        for reminder in self.reminders:      # check each reminder
             # skip if already done or notifying
            if reminder.get("done", False) or reminder.get("_notifying", False):
                continue
            snooze_until = reminder.get("snooze_until")  # get snooze time if any
            if snooze_until and now >= snooze_until:
                reminder["_notifying"] = True  
                self.notify_user(reminder)                      
            elif not snooze_until and now >= reminder["time"]: 
                reminder["_notifying"] = True 
                self.notify_user(reminder) 
        self.root.after(3000, self.check_reminders) # check every 3 seconds // 3000=3s

    # ================= Notify (popup) =================
    def notify_user(self, reminder):     # show popup and play sound
         # prevent multiple notifications for same reminder
        if self.alarm_active:
            return
        self.alarm_active = True  
        self.alarm_thread = threading.Thread(target=self.play_alarm_sound, daemon=True) 
        self.alarm_thread.start()  

        win = tk.Toplevel(self.root)
        win.title("⏰ Reminder") 
        win.geometry("420x220")
        win.resizable(False, False)
        try:
            win.transient(self.root)
            win.grab_set()
            win.focus_force()
            win.attributes("-topmost", True)
        except:
            pass

        tk.Label(win, text=f"It's time for:\n{reminder['title']}", font=self.FONT_TITLE).pack(pady=10)

        delay_frame = tk.Frame(win)
        delay_frame.pack(pady=5)
        tk.Label(delay_frame, text="Remind again in:").pack(side="left")
        delay_var = tk.StringVar(value=str(reminder.get("snooze_delay", 5)))
        delay_combo = ttk.Combobox(delay_frame, textvariable=delay_var, width=8, state="readonly")
        delay_combo['values'] = ("1", "5", "10", "15", "30", "60")
        delay_combo.pack(side="left", padx=5)
        tk.Label(delay_frame, text="minutes").pack(side="left")

        def mark_done():
            self.alarm_active = False
            reminder["_notifying"] = False
            reminder.pop("snooze_until", None)
            if reminder.get("repeat", False):
                reminder["time"] += timedelta(days=1)
                reminder["done"] = False
                status = "repeat-next-day"
            else:
                reminder["done"] = True
                status = "done"
            self.save_history({
                "title": reminder["title"],
                "time": reminder["time"].strftime("%Y-%m-%d %H:%M"),
                "notified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": status
            })
            self.save_reminders()
            self.update_reminder_list()
            win.destroy()
            messagebox.showinfo("Good job!", "You completed a task!")

        def remind_later():
            self.alarm_active = False
            reminder["_notifying"] = False
            try:
                delay_minutes = int(delay_var.get())
                reminder["snooze_until"] = datetime.now() + timedelta(minutes=delay_minutes)
                reminder["snooze_delay"] = delay_minutes
                reminder["done"] = False
                self.save_reminders()
                self.update_reminder_list()
                win.destroy()
                messagebox.showinfo("Snoozed", f"Reminder snoozed for {delay_minutes} minutes")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of minutes")

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="✅ Done", command=mark_done).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="⏰ Remind Later", command=remind_later).pack(side="right", padx=10)

    # ================= Reminder Operations =================
    def add_reminder(self):
        title = self.title_entry.get().strip()
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()
        time_str = self.time_entry.get().strip()
        repeat = self.repeat_var.get()
        category = self.category_entry.get().strip()
        snooze_delay = self.snooze_delay_var.get()

        if not title or not time_str:
            messagebox.showwarning("Input Error", "Please enter both title and time")
            return
        try:
            remind_time = datetime.strptime(f"{year}-{month}-{day} {time_str}", "%Y-%m-%d %H:%M")
            if remind_time < datetime.now():
                remind_time += timedelta(days=1)

            self.reminders.append({
                "title": title,
                "time": remind_time,
                "repeat": repeat,
                "category": category,
                "snooze_delay": snooze_delay,
                "done": False
            })
            self.save_reminders()
            self.update_reminder_list()
            self.title_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.repeat_var.set(False)
            self.snooze_delay_var.set(5)
        except ValueError:
            messagebox.showerror("Time Format Error", "Please enter time in HH:MM format")

    def delete_reminder(self, index):
        if 0 <= index < len(self.reminders):
            self.reminders.pop(index)
            self.save_reminders()
            self.update_reminder_list()

    def edit_reminder(self, index):
        if index < 0 or index >= len(self.reminders):
            return
        r = self.reminders[index]

        win = tk.Toplevel(self.root)
        win.title("✏️ Edit Reminder")
        win.geometry("350x350")

        tk.Label(win, text="Title:").pack(pady=2)
        title_e = ttk.Entry(win)
        title_e.pack(pady=2)
        title_e.insert(0, r["title"])

        tk.Label(win, text="Date (YYYY-MM-DD):").pack(pady=2)
        date_e = ttk.Entry(win)
        date_e.pack(pady=2)
        date_e.insert(0, r["time"].strftime("%Y-%m-%d"))

        tk.Label(win, text="Time (HH:MM):").pack(pady=2)
        time_e = ttk.Entry(win)
        time_e.pack(pady=2)
        time_e.insert(0, r["time"].strftime("%H:%M"))

        tk.Label(win, text="Category:").pack(pady=2)
        cat_e = ttk.Entry(win)
        cat_e.pack(pady=2)
        cat_e.insert(0, r.get("category", ""))

        tk.Label(win, text="Default Snooze Delay (minutes):").pack(pady=2)
        snooze_delay_e = ttk.Combobox(win, values=("1", "5", "10", "15", "30", "60"), state="readonly", width=10)
        snooze_delay_e.pack(pady=2)
        snooze_delay_e.set(str(r.get("snooze_delay", 5)))

        repeat_var_local = tk.BooleanVar(value=r.get("repeat", False))
        tk.Checkbutton(win, text="Repeat daily", variable=repeat_var_local).pack(pady=5)

        def save_changes():
            try:
                new_time = datetime.strptime(date_e.get() + " " + time_e.get(), "%Y-%m-%d %H:%M")
                r["title"] = title_e.get()
                r["time"] = new_time
                r["category"] = cat_e.get()
                r["repeat"] = repeat_var_local.get()
                r["snooze_delay"] = int(snooze_delay_e.get())
                r.pop("snooze_until", None)
                r["done"] = new_time <= datetime.now()
                self.save_reminders()
                self.update_reminder_list()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid date or time format!")

        ttk.Button(win, text="✅ Done", command=save_changes).pack(pady=10)

    # ================= Import/Export/Snoozed =================
    def show_snoozed_reminders(self):
        snoozed = [r for r in self.reminders if r.get("snooze_until")]
        if not snoozed:
            messagebox.showinfo("No Snoozed Reminders", "There are no snoozed reminders.")
            return
        win = tk.Toplevel(self.root)
        win.title("⏱️ Snoozed Reminders")
        win.geometry("400x300")
        win.resizable(False, False)
        frame = ttk.Frame(win, padding=10)
        frame.pack(fill="both", expand=True)
        for r in snoozed:
            time_str = r["time"].strftime("%Y-%m-%d %H:%M")
            snooze_str = r["snooze_until"].strftime("%Y-%m-%d %H:%M:%S")
            delay_minutes = r.get("snooze_delay", 5)
            label = tk.Label(frame, text=f"{r['title']} (🕒 {time_str})\nSnoozed until: {snooze_str}\nDefault delay: {delay_minutes} min", anchor="w", justify="left", font=self.FONT_NORMAL)
            label.pack(fill="x", pady=5, anchor="w")

    def import_reminders(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    imported = json.load(f)
                    for r in imported:
                        if isinstance(r.get("time"), str):
                            r["time"] = datetime.strptime(r["time"], "%Y-%m-%d %H:%M")
                        if "snooze_until" in r and isinstance(r["snooze_until"], str):
                            try:
                                r["snooze_until"] = datetime.strptime(r["snooze_until"], "%Y-%m-%d %H:%M:%S")
                            except:
                                r.pop("snooze_until", None)
                        r.setdefault("repeat", False)
                        r.setdefault("done", False)
                        r.setdefault("snooze_delay", 5)
                        if not any(existing["title"] == r["title"] and existing["time"] == r["time"] for existing in self.reminders):
                            self.reminders.append(r)
                self.save_reminders()
                self.update_reminder_list()
                messagebox.showinfo("Import Successful", f"Reminders imported from {file_path}")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import reminders:\n{e}")

    def export_reminders(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump([
                    {
                        **r,
                        "time": r["time"].strftime("%Y-%m-%d %H:%M"),
                        **({"snooze_until": r["snooze_until"].strftime("%Y-%m-%d %H:%M:%S")} if r.get("snooze_until") else {})
                    } for r in self.reminders
                ], f, indent=2)
            messagebox.showinfo("Export Successful", f"Reminders exported to {file_path}")

    # ================= UI =================
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=self.BG_COLOR, foreground=self.TEXT_COLOR)
        style.configure("TButton", font=self.FONT_NORMAL, padding=6)
        style.configure("Accent.TButton", background=self.ACCENT_COLOR, foreground="white")
        style.configure("Danger.TButton", background="#d40000", foreground="white")

        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="📌 Simple Reminder App", font=("Segoe UI", 14, "bold")).pack(side="left")

        # Add Reminder Section
        add_frame = ttk.LabelFrame(main_container, text="Add New Reminder", padding=10)
        add_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=2)
        self.title_entry = ttk.Entry(add_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 0), columnspan=3)

        ttk.Label(add_frame, text="Date:").grid(row=1, column=0, sticky="w", pady=2)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        self.month_var = tk.StringVar(value=f"{datetime.now().month:02}")
        self.day_var = tk.StringVar(value=f"{datetime.now().day:02}")
        year_menu = ttk.OptionMenu(add_frame, self.year_var, self.year_var.get(), *[str(y) for y in range(2020, 2035)])
        month_menu = ttk.OptionMenu(add_frame, self.month_var, self.month_var.get(), *[f"{m:02}" for m in range(1, 13)])
        day_menu = ttk.OptionMenu(add_frame, self.day_var, self.day_var.get(), *[f"{d:02}" for d in range(1, 32)])
        year_menu.grid(row=1, column=1, sticky="w", pady=2, padx=(5, 0))
        month_menu.grid(row=1, column=2, sticky="w", pady=2, padx=(5, 0))
        day_menu.grid(row=1, column=3, sticky="w", pady=2, padx=(5, 0))

        ttk.Label(add_frame, text="Time (HH:MM):").grid(row=2, column=0, sticky="w", pady=2)
        self.time_entry = ttk.Entry(add_frame, width=20)
        self.time_entry.grid(row=2, column=1, sticky="w", pady=2, padx=(5, 0))

        ttk.Label(add_frame, text="Category (or Note):").grid(row=3, column=0, sticky="w", pady=2)
        self.category_entry = ttk.Entry(add_frame, width=40)
        self.category_entry.grid(row=3, column=1, sticky="ew", pady=2, padx=(5, 0), columnspan=3)

        ttk.Label(add_frame, text="Snooze Delay (minutes):").grid(row=4, column=0, sticky="w", pady=2)
        self.snooze_delay_var = tk.IntVar(value=5)
        snooze_delay_combo = ttk.Combobox(add_frame, textvariable=self.snooze_delay_var, values=(1, 5, 10, 15, 30, 60), state="readonly", width=8)
        snooze_delay_combo.grid(row=4, column=1, sticky="w", pady=2, padx=(5, 0))
        ttk.Label(add_frame, text="Default delay when snoozing").grid(row=4, column=2, sticky="w", pady=2, padx=(5, 0))

        self.repeat_var = tk.BooleanVar()
        ttk.Checkbutton(add_frame, text="Repeat daily", variable=self.repeat_var).grid(row=5, column=1, sticky="w", pady=2, padx=(5, 0))

        add_btn = ttk.Button(add_frame, text="➕ Add Reminder", command=self.add_reminder, style="Accent.TButton")
        add_btn.grid(row=6, column=1, sticky="e", pady=(5, 0))

        # Import/Export/Snoozed buttons
        io_frame = ttk.Frame(main_container)
        io_frame.pack(fill="x", pady=(0, 15))

        ttk.Button(io_frame, text="📂 Import Reminders", command=self.import_reminders).pack(side="left", padx=(0,5))
        ttk.Button(io_frame, text="💾 Export Reminders", command=self.export_reminders).pack(side="left")
        ttk.Button(io_frame, text="⏱️ View Snoozed", command=self.show_snoozed_reminders).pack(side="left", padx=(5,0))

        # Reminder List
        list_frame = ttk.LabelFrame(main_container, text="Your Reminders", padding=5)
        list_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(list_frame, borderwidth=0, highlightthickness=0, bg=self.BG_COLOR)
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.reminder_frame = ttk.Frame(self.canvas, style="TFrame")
        self.reminder_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.reminder_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ================= Update Reminder List =================
    def update_reminder_list(self):
        for widget in self.reminder_frame.winfo_children():
            widget.destroy()

        for idx, reminder in enumerate(self.reminders):
            bg = self.CARD_BG
            if reminder.get("done", False):
                bg = self.DONE_BG
            elif reminder.get("snooze_until"):
                bg = self.SNOOZED_BG

            frame = tk.Frame(self.reminder_frame, bg=bg, bd=1, relief="raised", padx=5, pady=5)
            frame.pack(fill="x", pady=5, padx=5)

            def on_enter(e, f=frame):
                f.configure(bg=self.CARD_HOVER)
            def on_leave(e, f=frame, b=bg):
                f.configure(bg=b)
            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)

            time_str = reminder["time"].strftime("%Y-%m-%d %H:%M")
            status_text = ""
            if reminder.get("snooze_until"):
                snooze_time = reminder["snooze_until"].strftime("%H:%M:%S")
                status_text = f"⏰ Snoozed until {snooze_time}"

            tk.Label(frame, text=reminder["title"], font=self.FONT_TITLE, bg=bg).pack(anchor="w")
            tk.Label(frame, text=f"🕒 {time_str}  |  📂 {reminder.get('category','None')}", font=self.FONT_SMALL, fg="#555", bg=bg).pack(anchor="w")
            tk.Label(frame, text=f"⏱️ Default snooze: {reminder.get('snooze_delay', 5)} minutes", font=self.FONT_SMALL, fg="#666", bg=bg).pack(anchor="w")
            if status_text:
                tk.Label(frame, text=status_text, font=self.FONT_SMALL, fg="#888", bg=bg).pack(anchor="w")

            btn_frame = tk.Frame(frame, bg=bg)
            btn_frame.pack(anchor="e", pady=2)
            ttk.Button(btn_frame, text="✏️ Edit", command=lambda i=idx: self.edit_reminder(i)).pack(side="left", padx=2)
            ttk.Button(btn_frame, text="🗑️ Delete", command=lambda i=idx: self.delete_reminder(i)).pack(side="left", padx=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
