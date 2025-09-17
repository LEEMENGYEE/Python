import tkinter as tk
from tkinter import ttk, messagebox

class GPAHistoryWindow:
    def __init__(self, parent, history_data, load_callback):
        """
        Initialize the GPA History window
        parent: the parent window
        history_data: list of history entries
        load_callback: function to call when loading history
        """
        self.parent = parent
        self.history_data = history_data
        self.load_callback = load_callback
        
        # Create a new top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("GPA History")
        
        # Set window size and position
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Set history window size
        window_width = min(int(screen_width * 0.7), 900)
        window_height = min(int(screen_height * 0.6), 500)
        
        # Calculate position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        # Set window geometry and position
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.window.resizable(True, True)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', 
                            font=('Arial', 16, 'bold'),
                            foreground='#2c3e50')
        
        self.style.configure('History.TFrame', 
                           background='#f8f9fa',
                           relief=tk.RAISED,
                           borderwidth=1)
        
        # Create main container
        main_container = ttk.Frame(self.window, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_label = ttk.Label(main_container, 
                               text="GPA Calculation History", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 15))
        
        # Create frame for history list
        history_frame = ttk.LabelFrame(main_container, 
                                      text="Saved Calculations",
                                      padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar for history list
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(history_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Create frame inside canvas for history items
        self.history_container = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.history_container, anchor=tk.NW)
        
        # Bind events for scrolling and resizing
        self.history_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Display history items
        self.display_history()
    
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Reset the canvas window width to match canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def display_history(self):
        """Display all history entries"""
        # Clear existing history items
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        if not self.history_data:
            # Show message if no history
            no_history_label = ttk.Label(self.history_container, 
                                        text="No history available. Save some calculations first!",
                                        font=('Arial', 12),
                                        foreground='#7f8c8d')
            no_history_label.pack(pady=20)
            return
        
        # Display each history entry
        for i, entry in enumerate(self.history_data):
            self.create_history_item(entry, i)
    
    def create_history_item(self, entry, index):
        """Create a UI element for a history entry"""
        # Create frame for history item
        item_frame = ttk.Frame(self.history_container, style='History.TFrame')
        item_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Configure grid for item frame
        item_frame.columnconfigure(0, weight=1)
        
        # Display timestamp
        timestamp_label = ttk.Label(item_frame, 
                                   text=f"Saved: {entry['timestamp']}", 
                                   font=('Arial', 10, 'bold'),
                                   foreground='#2c3e50')
        timestamp_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Display GPA and total credits
        info_label = ttk.Label(item_frame, 
                              text=f"GPA: {entry['gpa']:.3f} | Total Credits: {entry['total_credits']}", 
                              font=('Arial', 9),
                              foreground='#34495e')
        info_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Display course count
        course_count = len(entry['courses'])
        course_label = ttk.Label(item_frame, 
                                text=f"Courses: {course_count}", 
                                font=('Arial', 9),
                                foreground='#7f8c8d')
        course_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Create button frame
        button_frame = ttk.Frame(item_frame)
        button_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky=tk.E)
        
        # Load button
        load_btn = ttk.Button(button_frame, 
                             text="Load", 
                             command=lambda e=entry: self.load_history(e),
                             width=8)
        load_btn.pack(side=tk.LEFT, padx=2)
        
        # View Details button
        details_btn = ttk.Button(button_frame, 
                                text="View Details", 
                                command=lambda e=entry: self.view_details(e),
                                width=12)
        details_btn.pack(side=tk.LEFT, padx=2)
        
        # Delete button
        delete_btn = ttk.Button(button_frame, 
                               text="Delete", 
                               command=lambda i=index: self.delete_history(i),
                               width=8)
        delete_btn.pack(side=tk.LEFT, padx=2)
    
    def load_history(self, entry):
        """Load a history entry"""
        self.load_callback(entry)
    
    def view_details(self, entry):
        """View details of a history entry"""
        # Create details window
        details_window = tk.Toplevel(self.window)
        details_window.title("History Details")
        details_window.geometry("500x400")
        details_window.resizable(True, True)
        
        # Create main container
        container = ttk.Frame(details_window, padding="10")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Display timestamp
        timestamp_label = ttk.Label(container, 
                                   text=f"Saved: {entry['timestamp']}", 
                                   font=('Arial', 12, 'bold'),
                                   foreground='#2c3e50')
        timestamp_label.pack(pady=(0, 10))
        
        # Display GPA and total credits
        info_label = ttk.Label(container, 
                              text=f"GPA: {entry['gpa']:.3f} | Total Credits: {entry['total_credits']}", 
                              font=('Arial', 11),
                              foreground='#34495e')
        info_label.pack(pady=(0, 15))
        
        # Create frame for course list
        course_frame = ttk.LabelFrame(container, text="Courses", padding="10")
        course_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar for course list
        scrollbar = ttk.Scrollbar(course_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox for courses
        course_listbox = tk.Listbox(course_frame, 
                                   yscrollcommand=scrollbar.set,
                                   font=('Arial', 10))
        course_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=course_listbox.yview)
        
        # Add courses to listbox
        for name, (credit, grade) in entry['courses'].items():
            course_listbox.insert(tk.END, f"{name}: {credit} credits, Grade: {grade}")
    
    def delete_history(self, index):
        """Delete a history entry"""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this history entry?"):
            # Remove from history data
            del self.history_data[index]
            
            # Refresh history display
            self.display_history()
            
            messagebox.showinfo("Success", "History entry deleted!")