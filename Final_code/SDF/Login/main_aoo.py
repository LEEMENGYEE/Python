import tkinter as tk
from tkinter import messagebox, ttk
import json
import sys
import os

# Ensure the parent directory is in sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Simple_Reminder_App.reminder import ReminderApp
from datetime import datetime



class LoginApp:
    def __init__(self, root, user=None):
        self.root = root
        self.root.title("TAR UMT Student Assistant App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(True, True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('TButton', font=('Arial', 11), padding=10)
        self.style.configure('Header.TLabel', font=('Arial', 22, 'bold'), background='#2c3e50', foreground='white')
        self.style.configure('Feature.TButton', font=('Arial', 14, 'bold'), padding=15)
        
        # Fixed login credentials
        self.fixed_email = "dft@gmail.com"
        self.fixed_password = "123456"
        
        # Current user state
        self.logged_in = False
        self.current_user = None
        
        # Load initial data
        self.create_main_interface()
    
    def create_main_interface(self):
        # Header with gradient background
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Project name with better styling
        title_label = tk.Label(header_frame, text="🎓 TAR UMT Student Assistant", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Login button with modern style
        self.login_btn = tk.Button(header_frame, text="Login", font=('Arial', 12, 'bold'), 
                                  command=self.show_login, bg='#3498db', fg='white', 
                                  relief=tk.FLAT, padx=25, pady=8,
                                  activebackground='#2980b9', activeforeground='white',
                                  cursor='hand2')
        self.login_btn.pack(side=tk.RIGHT, padx=55, pady=20)
        
        # Welcome section
        welcome_frame = tk.Frame(self.root, bg='#f8f9fa')
        welcome_frame.pack(fill=tk.X, pady=(20, 30))
        
        welcome_label = tk.Label(welcome_frame, text="Welcome to Student Assistant", 
                                font=('Arial', 18, 'bold'), fg='#2c3e50', bg='#f8f9fa')
        welcome_label.pack()
        
        subtitle_label = tk.Label(welcome_frame, text="Your all-in-one campus companion", 
                                 font=('Arial', 12), fg='#7f8c8d', bg='#f8f9fa')
        subtitle_label.pack(pady=(5, 0))
        
        # Main content area with better spacing
        content_frame = tk.Frame(self.root, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Feature buttons with improved design
        features = [
            ("📊 GPA Calculator", self.open_gpa_calculator, '#e74c3c'),
            ("⏰ Simple Reminder", self.open_reminder, '#3498db'),
            ("🏢 Booking Discussion Room", self.open_booking, '#2ecc71'),
            ("⚙ Settings", self.open_settings, '#9b59b6')
        ]
        
        for i, (text, command, color) in enumerate(features):
            btn_frame = tk.Frame(content_frame, bg='#f8f9fa')
            btn_frame.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")
            
            btn = tk.Button(btn_frame, text=text, font=('Arial', 14, 'bold'), 
                           command=command, bg=color, fg='white',
                           width=22, height=2, relief=tk.FLAT, bd=0,
                           activebackground=color, activeforeground='white',
                           cursor='hand2')
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, btn=btn, color=color: 
                    btn.config(bg=self.lighten_color(color)))
            btn.bind("<Leave>", lambda e, btn=btn, color=color: 
                    btn.config(bg=color))
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#34495e', height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(footer_frame, text="© 2025 TAR UMT Student Assistant App", 
                               font=('Arial', 10), fg='white', bg='#34495e')
        footer_label.pack(pady=15)
    
    def lighten_color(self, color):
        # Convert hex to RGB and lighten
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        lighter = tuple(min(255, c + 30) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'
    
    def show_login(self):
        if self.logged_in:
            self.logout()
            return
        
        login_window = tk.Toplevel(self.root)
        login_window.title("Login - TAR UMT Student Assistant")
        login_window.geometry("450x400")
        login_window.configure(bg='#ecf0f1')
        login_window.resizable(False, False)
        login_window.transient(self.root)
        login_window.grab_set()
        
        # Center the window
        login_window.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        login_window.geometry(f"450x400+{x}+{y}")
        
        # Login header
        login_header = tk.Frame(login_window, bg='#2c3e50', height=80)
        login_header.pack(fill=tk.X)
        login_header.pack_propagate(False)
        
        login_title = tk.Label(login_header, text="🔐 Login", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        login_title.pack(pady=25)
        
        # Login form with better styling
        form_frame = tk.Frame(login_window, bg='#ecf0f1')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Email field
        email_frame = tk.Frame(form_frame, bg='#ecf0f1')
        email_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(email_frame, text="Email Address", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor=tk.W)
        
        email_entry = tk.Entry(email_frame, font=('Arial', 12), 
                              relief=tk.FLAT, bd=2, bg='white')
        email_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        email_entry.insert(0, "dft@gmail.com")
        email_entry.config(fg='#7f8c8d')
        
        # Password field
        password_frame = tk.Frame(form_frame, bg='#ecf0f1')
        password_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(password_frame, text="Password", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor=tk.W)
        
        password_entry = tk.Entry(password_frame, font=('Arial', 12), 
                                 show='*', relief=tk.FLAT, bd=2, bg='white')
        password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        password_entry.insert(0, "123456")
        password_entry.config(fg='#7f8c8d', show='')
        
        # Login button
        login_btn = tk.Button(form_frame, text="Login", font=('Arial', 12, 'bold'),
                             command=lambda: self.validate_login(
                                 email_entry.get(), 
                                 password_entry.get(), 
                                 login_window
                             ), bg='#27ae60', fg='white', relief=tk.FLAT,
                             padx=20, pady=22, cursor='hand2',
                             activebackground='#229954', activeforeground='white')
        login_btn.pack(pady=10)
        
        # Hint text
        hint_label = tk.Label(form_frame, text="Default: dft@gmail.com / 123456", 
                             font=('Arial', 9), fg='#7f8c8d', bg='#ecf0f1')
        hint_label.pack()
    
    def validate_login(self, email, password, window):
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if email == self.fixed_email and password == self.fixed_password:
            self.logged_in = True
            self.current_user = email
            self.login_btn.config(text="Logout", bg='#e74c3c', activebackground='#c0392b')
            window.destroy()
            messagebox.showinfo("Success", "Logged in successfully!")
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def is_valid_email(self, email):
        return '@' in email and '.' in email.split('@')[-1]
    
    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.login_btn.config(text="Login", bg='#3498db', activebackground='#2980b9')
        messagebox.showinfo("Success", "Logged out successfully!")
    
    def check_login(self):
        if not self.logged_in:
            messagebox.showinfo("Login Required", "Please login to access this feature")
            return False
        return True
    
    def open_gpa_calculator(self):
     if self.check_login():
        try:
            import tkinter as tk
            import tkinter.ttk as ttk
            from Calculator.gpa_calculator_main import GPACalculator

            gpa_window = tk.Toplevel(self.root)
            gpa_window.title("GPA Module")
            gpa_window.geometry("900x700")

            # Notebook
            notebook = ttk.Notebook(gpa_window)
            notebook.pack(fill="both", expand=True)

            # Calculator Tab
            calc_frame = ttk.Frame(notebook)
            notebook.add(calc_frame, text="Calculator")
            self.gpa_calculator = GPACalculator(calc_frame)

        except ImportError as e:
            messagebox.showerror("Error", f"Module not found:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open GPA Module:\n{e}")

    def open_reminder(self):
        if not self.check_login():
            return
        try:
            reminder_window = tk.Toplevel(self.root)
            reminder_window.title("⏰ Simple Reminder App")
            reminder_window.geometry("800x800")
            reminder_window.configure(bg="#f5f7fa")
            reminder_window.resizable(True, True)
            from Simple_Reminder_App.reminder import ReminderApp
            reminder_app = ReminderApp(reminder_window)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open Reminder App:\n{e}")

    def open_booking(self):
        if not self.check_login():
            return
        try:
            from BookingRoom.booking_system import BookingSystem
            booking_window = tk.Toplevel(self.root)
            booking_window.title("Booking System")
            booking_window.geometry("1300x750")
            booking_app = BookingSystem(booking_window, self.current_user)
        except ImportError:
            messagebox.showerror("Error", "Booking System module not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open Booking System:\n{e}")

    def open_settings(self):
        if not self.check_login():
            return
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x450")
        settings_window.configure(bg='#ecf0f1')
        settings_window.resizable(False, False)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (450 // 2)
        settings_window.geometry(f"500x450+{x}+{y}")
        
        # Settings header
        header_frame = tk.Frame(settings_window, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="⚙ Settings", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(settings_window, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # User info
        user_frame = tk.Frame(main_frame, bg='#ecf0f1')
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(user_frame, text=f"Logged in as: {self.current_user}", 
                font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#ecf0f1').pack(anchor=tk.W)
        
        # Password reset section
        reset_frame = tk.LabelFrame(main_frame, text="Reset Password", 
                                  font=('Arial', 12, 'bold'), bg='#ecf0f1',
                                  fg='#2c3e50', relief=tk.GROOVE, bd=1)
        reset_frame.pack(fill=tk.X, pady=10)
        
        # Current password
        tk.Label(reset_frame, text="Current Password:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        current_pass = tk.Entry(reset_frame, font=('Arial', 10), show='*', 
                               relief=tk.FLAT, bd=1, bg='white')
        current_pass.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=10, ipady=4)
        
        # New password
        tk.Label(reset_frame, text="New Password:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        new_pass = tk.Entry(reset_frame, font=('Arial', 10), show='*', 
                           relief=tk.FLAT, bd=1, bg='white')
        new_pass.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=10, ipady=4)
        
        # Confirm new password
        tk.Label(reset_frame, text="Confirm Password:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        confirm_pass = tk.Entry(reset_frame, font=('Arial', 10), show='*', 
                               relief=tk.FLAT, bd=1, bg='white')
        confirm_pass.grid(row=2, column=1, sticky=tk.EW, padx=10, pady=10, ipady=4)
        
        reset_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=20)
        
        reset_btn = tk.Button(button_frame, text="Reset Password", font=('Arial', 11, 'bold'),
                            command=lambda: self.reset_password(
                                current_pass.get(),
                                new_pass.get(),
                                confirm_pass.get(),
                                settings_window
                            ), bg='#e74c3c', fg='white', relief=tk.FLAT,
                            padx=15, pady=8, cursor='hand2',
                            activebackground='#c0392b', activeforeground='white')
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="Close", font=('Arial', 11),
                            command=settings_window.destroy, bg='#95a5a6', fg='white',
                            relief=tk.FLAT, padx=15, pady=8, cursor='hand2',
                            activebackground='#7f8c8d', activeforeground='white')
        close_btn.pack(side=tk.RIGHT)
        
        current_pass.focus_set()
        
    def reset_password(self, current_password, new_password, confirm_password, window):
        # Validation logic remains the same
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if current_password != self.fixed_password:
            messagebox.showerror("Error", "Current password is incorrect")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters")
            return
        
        if current_password == new_password:
            messagebox.showerror("Error", "New password must be different from current password")
            return
        
        self.fixed_password = new_password
        messagebox.showinfo("Success", "Password reset successfully!")
        window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()