import tkinter as tk
from tkinter import ttk

class GPAChartWindow:
    def __init__(self, parent, courses, grade_points, grade_colors):
        """
        Initialize the GPA Chart window
        parent: the parent window
        courses: dictionary of courses
        grade_points: grade point mapping
        grade_colors: color mapping for grades
        """
        self.parent = parent
        self.courses = courses
        self.grade_points = grade_points
        self.grade_colors = grade_colors
        
        # Create a new top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Academic Performance Chart")
        
        # Set window size and position
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Set chart window size to 60% of screen size
        window_width = min(int(screen_width * 0.6), 800)
        window_height = min(int(screen_height * 0.6), 600)
        
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
        
        # Create main container
        main_container = ttk.Frame(self.window, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        title_label = ttk.Label(main_container, 
                               text="Academic Performance Chart", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 15))
        
        # Create canvas for the chart
        self.chart_canvas = tk.Canvas(main_container, bg='white')
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw the performance chart
        self.draw_performance_chart()
        
        # Bind window resize event
        self.window.bind('<Configure>', self.on_window_resize)
    
    def on_window_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.window:
            self.draw_performance_chart()
    
    def draw_performance_chart(self):
        """Draw a bar chart showing performance for each course"""
        # Clear the canvas
        self.chart_canvas.delete("all")
        
        if not self.courses:
            # Show message if no courses
            canvas_width = self.chart_canvas.winfo_width()
            canvas_height = self.chart_canvas.winfo_height()
            self.chart_canvas.create_text(canvas_width // 2, canvas_height // 2, 
                                         text="No courses to display",
                                         fill="#7f8c8d",
                                         font=('Arial', 14))
            return
        
        # Get canvas dimensions
        canvas_width = self.chart_canvas.winfo_width()
        canvas_height = self.chart_canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10:
            # Canvas not yet rendered, try again later
            self.window.after(100, self.draw_performance_chart)
            return
        
        # Calculate bar dimensions
        num_courses = len(self.courses)
        margin = 50
        chart_width = canvas_width - 2 * margin
        bar_width = min(40, (chart_width - 20) // max(1, num_courses))
        spacing = (chart_width - (num_courses * bar_width)) // max(1, num_courses + 1)
        
        # Draw chart title
        self.chart_canvas.create_text(canvas_width // 2, 20, 
                                     text="Course Performance", 
                                     font=('Arial', 14, 'bold'),
                                     fill='#2c3e50')
        
        # Draw horizontal axis
        axis_y = canvas_height - 50
        self.chart_canvas.create_line(margin, axis_y, canvas_width - margin, axis_y, fill='black', width=2)
        
        # Draw bars for each course
        course_names = list(self.courses.keys())
        max_grade = 4.0  # Maximum possible grade
        
        for i, course_name in enumerate(course_names):
            credit, grade = self.courses[course_name]
            grade_point = self.grade_points[grade]
            
            # Calculate bar position and dimensions
            x = margin + spacing + i * (bar_width + spacing)
            bar_height = (grade_point / max_grade) * (axis_y - 70)
            y = axis_y - bar_height
            
            # Draw the bar
            color = self.grade_colors.get(grade, "#3498db")
            self.chart_canvas.create_rectangle(x, y, x + bar_width, axis_y, 
                                              fill=color, outline='black', width=1)
            
            # Draw grade value above the bar
            self.chart_canvas.create_text(x + bar_width / 2, y - 15, 
                                         text=f"{grade_point}", 
                                         font=('Arial', 10, 'bold'),
                                         fill='black')
            
            # Draw course name below the bar (truncate if too long)
            display_name = course_name[:12] + "..." if len(course_name) > 12 else course_name
            self.chart_canvas.create_text(x + bar_width / 2, axis_y + 20, 
                                         text=display_name, 
                                         font=('Arial', 9),
                                         fill='black',
                                         angle=45 if len(course_names) > 5 else 0)
        
        # Draw vertical axis with grade markers
        self.chart_canvas.create_line(margin, 50, margin, axis_y, fill='black', width=2)
        for i in range(5):
            value = i
            y = axis_y - (value / max_grade) * (axis_y - 70)
            self.chart_canvas.create_line(margin - 5, y, margin, y, fill='black')
            self.chart_canvas.create_text(margin - 15, y, 
                                         text=str(value), 
                                         font=('Arial', 10),
                                         fill='black')
        
        # Draw axis labels
        self.chart_canvas.create_text(margin - 30, (axis_y + 50) // 2, 
                                     text="Grade Points", 
                                     font=('Arial', 10),
                                     fill='black',
                                     angle=90)
        
        self.chart_canvas.create_text(canvas_width // 2, axis_y + 40, 
                                     text="Courses", 
                                     font=('Arial', 10),
                                     fill='black')
        
        # Draw legend
        legend_x = canvas_width - 150
        legend_y = 60
        self.chart_canvas.create_text(legend_x, legend_y - 20, 
                                     text="Grade Legend", 
                                     font=('Arial', 10, 'bold'),
                                     fill='black')
        
        grades = list(self.grade_colors.keys())
        for i, grade in enumerate(grades):
            y_pos = legend_y + i * 20
            self.chart_canvas.create_rectangle(legend_x - 50, y_pos - 8, 
                                              legend_x - 40, y_pos + 2,
                                              fill=self.grade_colors[grade], 
                                              outline='black')
            self.chart_canvas.create_text(legend_x - 20, y_pos - 3, 
                                         text=grade, 
                                         font=('Arial', 9),
                                         fill='black',
                                         anchor=tk.W)