# gpa_calculator_main.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from Calculator.gpa_chart import GPAChartWindow
from Calculator.gpa_history import GPAHistoryWindow


class GPACalculator:
    def __init__(self, parent):
        """
        Initialize the GPA Calculator tab
        parent: the Frame provided by main_aoo.py (inside Notebook)
        """
        self.root = parent   # parent is the Frame from main app

        # Apply a modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('Title.TLabel', 
                            font=('Arial', 18, 'bold'),
                            foreground='#2c3e50')

        self.style.configure('Section.TLabel',
                            font=('Arial', 12, 'bold'),
                            foreground='#34495e')

        self.style.configure('TButton',
                            font=('Arial', 10),
                            padding=5,
                            background='#3498db',
                            foreground='white')

        self.style.map('TButton',
                      background=[('active', '#2980b9')])

        self.style.configure('TEntry', padding=5)

        # Data structure to store course information
        self.courses = {}
        self.history_data = []

        # Grade point mapping
        self.grade_points = {
            "A+": 4.0, "A": 4.0, "A-": 3.67,
            "B+": 3.33, "B": 3.0, "B-": 2.67,
            "C+": 2.33, "C": 2.0, "F": 0.0
        }

        # Grade colors
        self.grade_colors = {
            "A+": "#27ae60", "A": "#27ae60", "A-": "#2ecc71",
            "B+": "#f1c40f", "B": "#f39c12", "B-": "#e67e22",
            "C+": "#e74c3c", "C": "#c0392b", "F": "#7f8c8d"
        }

        self.MAX_CREDIT_HOURS = 10
        self.chart_window = None
        self.history_window = None

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components"""
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_container, 
                               text="📘 GPA Calculator", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 15))

        
        # Create input section with a labeled frame
        input_frame = ttk.LabelFrame(main_container, 
                                    text="Add New Course",
                                    padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configure grid for input fields
        input_frame.columnconfigure(1, weight=1)
        
        # Course name input
        ttk.Label(input_frame, text="Course Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.course_name = ttk.Entry(input_frame, width=25)
        self.course_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Credit hours input with maximum limit note
        ttk.Label(input_frame, text="Credit Hours (max 10):").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.credit_hours = ttk.Entry(input_frame, width=25)
        self.credit_hours.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Grade selection
        ttk.Label(input_frame, text="Grade:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.grade_var = tk.StringVar(self.root)
        self.grade_var.set("A")  # default value
        # Get the list of available grades from the grade_points dictionary
        available_grades = list(self.grade_points.keys())
        grade_dropdown = ttk.Combobox(input_frame, 
                                     textvariable=self.grade_var,
                                     values=available_grades,
                                     state="readonly",
                                     width=22)
        grade_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Button to add course
        add_btn = ttk.Button(input_frame, text="Add Course", command=self.add_course)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Create a frame for the course list
        list_frame = ttk.LabelFrame(main_container, 
                                   text="Course List",
                                   padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create a scrollbar for the listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox to display courses
        self.course_listbox = tk.Listbox(list_frame, 
                                        width=50, 
                                        height=10, 
                                        yscrollcommand=scrollbar.set,
                                        font=('Arial', 10),
                                        selectbackground="#7dc5f4",
                                        selectforeground='white')
        self.course_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.course_listbox.yview)
        
        # Button to remove selected course
        remove_btn = ttk.Button(list_frame, text="Remove Selected", command=self.remove_course)
        remove_btn.pack(pady=5)
        
        # Button frame for actions
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Calculate GPA button
        calc_btn = ttk.Button(button_frame, text="Calculate GPA", command=self.calculate_gpa)
        calc_btn.grid(row=0, column=0, padx=5, sticky=tk.EW)
        
        # Save to History button
        save_btn = ttk.Button(button_frame, text="Save to History", command=self.save_to_history)
        save_btn.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        # View History button
        history_btn = ttk.Button(button_frame, text="View History", command=self.view_history)
        history_btn.grid(row=0, column=2, padx=5, sticky=tk.EW)
        
        # View Chart button
        chart_btn = ttk.Button(button_frame, text="View Performance Chart", command=self.open_chart_window)
        chart_btn.grid(row=0, column=3, padx=5, sticky=tk.EW)
        
        # Clear all button
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=4, padx=5, sticky=tk.EW)
        
        # Configure button frame columns to expand equally
        for i in range(5):
            button_frame.columnconfigure(i, weight=1)
        
        # Result display area
        result_frame = ttk.LabelFrame(main_container, 
                                     text="Results",
                                     padding="10")
        result_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.result_label = ttk.Label(result_frame, 
                                     text="Your GPA will be displayed here", 
                                     font=('Arial', 12),
                                     foreground='#3498db',
                                     background='#f0f0f0')
        self.result_label.pack()
        
        # Status bar at the bottom
        status_bar = ttk.Frame(main_container, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_bar, 
                                     text="Ready", 
                                     foreground='#7f8c8d',
                                     font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Set focus to the first entry field
        self.course_name.focus()
    
    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))  # Reset after 3 seconds
    
    def open_chart_window(self):
        """Open a new window to display the performance chart"""
        if not self.courses:
            messagebox.showinfo("Info", "No courses added to display chart!")
            return
            
        # Close existing chart window if open
        if self.chart_window and self.chart_window.window and self.chart_window.window.winfo_exists():
            self.chart_window.window.destroy()
            
        # Create new chart window
        self.chart_window = GPAChartWindow(self.root, self.courses, self.grade_points, self.grade_colors)
    
    def view_history(self):
        """Open a new window to view saved history"""
        # Close existing history window if open
        if self.history_window and self.history_window.window and self.history_window.window.winfo_exists():
            self.history_window.window.destroy()
            
        # Create new history window
        self.history_window = GPAHistoryWindow(self.root, self.history_data, self.load_from_history)
    
    def save_to_history(self):
        """Save current courses and GPA to history"""
        if not self.courses:
            messagebox.showinfo("Info", "No courses to save!")
            return
            
        # Calculate GPA
        total_quality_points = 0
        total_credits = 0
        
        for name, (credit, grade) in self.courses.items():
            grade_point = self.grade_points.get(grade, 0)
            total_quality_points += credit * grade_point
            total_credits += credit
        
        if total_credits == 0:
            messagebox.showerror("Error", "Total credits cannot be zero!")
            return
            
        gpa = total_quality_points / total_credits
        
        # Create history entry
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "courses": self.courses.copy(),
            "gpa": gpa,
            "total_credits": total_credits
        }
        
        # Add to history
        self.history_data.append(history_entry)
        
        messagebox.showinfo("Success", "Current data saved to history!")
        self.update_status("Data saved to history")
    
    def load_from_history(self, history_entry):
        """Load courses from a history entry"""
        # Clear current courses
        self.courses.clear()
        self.course_listbox.delete(0, tk.END)
        
        # Load courses from history
        self.courses = history_entry["courses"].copy()
        
        # Add courses to listbox
        for name, (credit, grade) in self.courses.items():
            display_text = f"{name}: {credit} credits, Grade: {grade}"
            self.course_listbox.insert(tk.END, display_text)
        
        # Update GPA display
        self.result_label.config(
            text=f"Your GPA is: {history_entry['gpa']:.3f}",
            foreground='#3498db',
            font=('Arial', 12)
        )
        
        self.update_status("Data loaded from history")
        
        # Close history window if open
        if self.history_window and self.history_window.window and self.history_window.window.winfo_exists():
            self.history_window.window.destroy()
    
    def add_course(self):
        """Add a new course to the list"""
        try:
            # Get values from input fields
            name = self.course_name.get().strip()
            credit_text = self.credit_hours.get().strip()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Course name cannot be empty!")
                return
                
            if not credit_text:
                messagebox.showerror("Error", "Credit hours cannot be empty!")
                return
                
            # Convert to float and validate
            credit = float(credit_text)
            
            if credit <= 0:
                messagebox.showerror("Error", "Credit hours must be positive!")
                return
                
            # Check if credit hours exceed maximum limit
            if credit > self.MAX_CREDIT_HOURS:
                messagebox.showerror("Error", 
                                   f"Credit hours cannot exceed {self.MAX_CREDIT_HOURS}!")
                return
                
            grade = self.grade_var.get()
            
            # Check if course already exists
            if name in self.courses:
                if messagebox.askyesno("Confirm", 
                                      f"Course '{name}' already exists. Do you want to replace it?"):
                    # Find and remove the existing course from listbox
                    for i in range(self.course_listbox.size()):
                        if self.course_listbox.get(i).startswith(name + ":"):
                            self.course_listbox.delete(i)
                            break
                else:
                    return
                
            # Add course to dictionary
            self.courses[name] = (credit, grade)
            
            # Add course to listbox
            display_text = f"{name}: {credit} credits, Grade: {grade}"
            self.course_listbox.insert(tk.END, display_text)
            
            # Clear input fields
            self.course_name.delete(0, tk.END)
            self.credit_hours.delete(0, tk.END)
            self.course_name.focus()  # Set focus back to course name
            
            self.update_status(f"Course '{name}' added successfully")
            
        except ValueError:
            # Exception handling for invalid input
            messagebox.showerror("Error", "Please enter valid credit hours (numeric value)!")
            self.credit_hours.focus()
    
    def remove_course(self):
        """Remove the selected course from the list"""
        try:
            # Get selected course index
            selection = self.course_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a course to remove!")
                return
                
            # Get the index of selected item
            index = selection[0]
            
            # Get course name from display text
            display_text = self.course_listbox.get(index)
            course_name = display_text.split(":")[0].strip()
            
            # Remove from dictionary and listbox
            if course_name in self.courses:
                del self.courses[course_name]
                self.course_listbox.delete(index)
                self.update_status(f"Course '{course_name}' removed")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def calculate_gpa(self):
        """Calculate the GPA based on added courses"""
        if not self.courses:
            messagebox.showinfo("Info", "No courses added to calculate GPA!")
            return
            
        total_quality_points = 0
        total_credits = 0
        
        # Loop through all courses and calculate GPA
        for name, (credit, grade) in self.courses.items():
            grade_point = self.grade_points.get(grade, 0)
            total_quality_points += credit * grade_point
            total_credits += credit
        
        # Calculate GPA
        if total_credits > 0:
            gpa = total_quality_points / total_credits
            
            # Determine GPA color based on value
            if gpa >= 3.5:
                color = "#27ae60"  # Green for excellent
            elif gpa >= 3.0:
                color = "#f39c12"  # Orange for good
            elif gpa >= 2.0:
                color = "#e67e22"  # Dark orange for satisfactory
            else:
                color = "#e74c3c"  # Red for needs improvement
                
            self.result_label.config(
                text=f"Your GPA is: {gpa:.3f}",
                foreground=color,
                font=('Arial', 12, 'bold')
            )
            
            # Provide additional feedback based on GPA
            if gpa >= 3.5:
                feedback = "Excellent performance! 🎉"
            elif gpa >= 3.0:
                feedback = "Good performance! 👍"
            elif gpa >= 2.0:
                feedback = "Satisfactory performance. 🙂"
            else:
                feedback = "Needs improvement. 📚"
                
            messagebox.showinfo("GPA Result", f"Your GPA is: {gpa:.3f}\n\n{feedback}")
            self.update_status(f"GPA calculated: {gpa:.3f}")
                
        else:
            messagebox.showerror("Error", "Total credits cannot be zero!")
    
    def clear_all(self):
        """Clear all courses and reset the calculator"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.courses.clear()
            self.course_listbox.delete(0, tk.END)
            self.result_label.config(
                text="Your GPA will be displayed here", 
                foreground='#3498db',
                font=('Arial', 12)
            )
            self.update_status("All data cleared")
            
            # Close chart window if open
            if self.chart_window and self.chart_window.window and self.chart_window.window.winfo_exists():
                self.chart_window.window.destroy()

