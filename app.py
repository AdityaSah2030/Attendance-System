import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime
import os

class AttendanceSystem:
    """
    A smartphone-oriented attendance management system.
    Features:
    - Single-column class list with alternating colors
    - Two-column student attendance grid
    - Intelligent column detection for Excel files
    - Simple and clean tile design
    """
    
    # Constants for UI configuration
    WINDOW_WIDTH = 480
    WINDOW_HEIGHT = 800
    TILE_WIDTH = 200
    TILE_HEIGHT = 80
    
    # Colors
    COLORS = {
        'white': '#FFFFFF',
        'black': '#2C3E50',
        'absent': '#E74C3C',
        'present': '#2ECC71',
        'text_dark': '#FFFFFF',
        'text_light': '#000000',
        'save_button': '#27AE60'
    }

    def __init__(self):
        """Initialize the attendance system and set up the main window."""
        self.setup_main_window()
        self.initialize_data_structures()
        self.create_main_screen()

    def setup_main_window(self):
        """Configure the main application window."""
        self.root = tk.Tk()
        self.root.title("Class Attendance")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, True)

    def initialize_data_structures(self):
        """Initialize data storage dictionaries."""
        self.classes_data = {}        # Stores class information and Excel data
        self.attendance_records = {}   # Stores daily attendance records
        self.student_buttons = {}      # Stores references to student buttons

    def create_main_screen(self):
        """Create the main screen with class list."""
        # Visual box for "Add Class" section at the bottom
        add_class_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        add_class_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        
        add_btn = tk.Button(
            add_class_frame,
            text="+ Add Class",
            font=('Roboto', 14),
            command=self.add_new_class,
            height=2,
            relief="flat",
            bd=0,
            bg=self.COLORS['save_button'],
            fg=self.COLORS['text_dark']
        )
        add_btn.pack(fill=tk.X)
        add_btn.bind("<ButtonPress-1>", self.animate_press)
        add_btn.bind("<ButtonRelease-1>", self.animate_release)
        
        # Scrollable class list (upper area)
        self.classes_frame = tk.Frame(self.root)
        self.classes_frame.pack(fill=tk.BOTH, expand=True, padx=10)

    def add_new_class(self):
        """Handle adding a new class from Excel file."""
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return
            
        try:
            # Load and process Excel file
            df = pd.read_excel(file_path)
            if "Total" not in df.columns:
                df["Total"] = 0
            class_name = os.path.basename(file_path).split('.')[0]
            
            # Detect data columns
            roll_col, name_col = self.detect_data_columns(df)
            
            # Reorder columns so that "Total" is always before the date columns
            other_columns = [col for col in df.columns if col not in [roll_col, name_col, "Total"]]
            df = df[[roll_col, name_col, "Total"] + other_columns]
            
            # Store class data
            self.classes_data[class_name] = {
                'dataframe': df,
                'file_path': file_path,
                'roll_column': roll_col,
                'name_column': name_col
            }
            
            self.create_class_tile(class_name)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load class: {str(e)}")

    def detect_data_columns(self, df):
        """
        Detect roll number and name columns in Excel file.
        Returns: (roll_column, name_column)
        """
        roll_patterns = ['roll', 'enrollment', 'id', 'number']
        name_patterns = ['name', 'student']
        
        roll_col = name_col = None
        
        # Search through column names
        for col in df.columns:
            col_lower = str(col).lower()
            if not roll_col and any(pattern in col_lower for pattern in roll_patterns):
                roll_col = col
            elif not name_col and any(pattern in col_lower for pattern in name_patterns):
                name_col = col
        
        # Default to first two columns if not found
        return roll_col or df.columns[0], name_col or df.columns[1]

    def create_class_tile(self, class_name):
        """Create a class tile with alternating colors."""
        tile_count = len(self.classes_data)
        bg_color = self.COLORS['white'] if tile_count % 2 == 0 else self.COLORS['black']
        text_color = self.COLORS['text_light'] if tile_count % 2 == 0 else self.COLORS['text_dark']
        
        tile = tk.Button(
            self.classes_frame,
            text=class_name,
            font=('Roboto', 16),
            bg=bg_color,
            fg=text_color,
            height=3,
            relief="flat",
            bd=1,
            command=lambda: self.open_attendance_screen(class_name)
        )
        tile.pack(fill=tk.X, pady=5)
        tile.bind("<ButtonPress-1>", self.animate_press)
        tile.bind("<ButtonRelease-1>", self.animate_release)

    def open_attendance_screen(self, class_name):
        """Open attendance screen for a class."""
        # Create attendance window
        attendance_window = tk.Toplevel(self.root)
        attendance_window.title(class_name)
        attendance_window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        attendance_window.resizable(False, True)
        
        # Initialize attendance records
        if class_name not in self.attendance_records:
            self.attendance_records[class_name] = {}
        
        # Create scrollable container
        container = tk.Frame(attendance_window)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Student grid (tiles expand to fill available space)
        self.create_student_grid(container, class_name)
        
        # SAVE button at bottom
        save_btn = tk.Button(
            attendance_window,
            text="SAVE",
            font=('Roboto', 16, 'bold'),
            bg=self.COLORS['save_button'],
            fg=self.COLORS['text_dark'],
            height=2,
            relief="flat",
            bd=1,
            command=lambda: self.save_attendance(class_name, attendance_window)
        )
        save_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        save_btn.bind("<ButtonPress-1>", self.animate_press)
        save_btn.bind("<ButtonRelease-1>", self.animate_release)

    def create_student_grid(self, container, class_name):
        """Create a two-column grid of student tiles."""
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns to expand fully
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        # Get student data
        df = self.classes_data[class_name]['dataframe']
        roll_col = self.classes_data[class_name]['roll_column']
        name_col = self.classes_data[class_name]['name_column']
        
        # Create student tiles in 2 columns
        self.student_buttons[class_name] = {}
        for index, row in df.iterrows():
            student_id = str(row[roll_col])
            grid_row = index // 2
            grid_col = index % 2
            
            # Create student tile with a frame and button for a softer look
            frame = tk.Frame(scrollable_frame, bd=1, relief="groove")
            frame.grid(row=grid_row, column=grid_col, padx=5, pady=5, sticky="nsew")
            
            button = tk.Button(
                frame,
                text=f"{student_id}\n{row[name_col]}",
                width=15,
                height=3,
                bg=self.COLORS['absent'],
                fg=self.COLORS['text_dark'],
                font=('Roboto', 12),
                relief="flat",
                bd=1,
                command=lambda sid=student_id: self.toggle_attendance(class_name, sid)
            )
            button.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            button.bind("<ButtonPress-1>", self.animate_press)
            button.bind("<ButtonRelease-1>", self.animate_release)
            
            self.student_buttons[class_name][student_id] = button
            self.attendance_records[class_name][student_id] = False

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def animate_press(self, event):
        """Simulate button press animation."""
        event.widget.config(relief="sunken")

    def animate_release(self, event):
        """Simulate button release animation."""
        event.widget.config(relief="flat")

    def toggle_attendance(self, class_name, student_id):
        """Toggle student attendance status."""
        current_status = self.attendance_records[class_name][student_id]
        self.attendance_records[class_name][student_id] = not current_status
        
        # Update button color
        button = self.student_buttons[class_name][student_id]
        button.configure(
            bg=self.COLORS['present'] if not current_status else self.COLORS['absent']
        )

    def save_attendance(self, class_name, attendance_window):
        """Save attendance records to Excel file."""
        try:
            df = self.classes_data[class_name]['dataframe'].copy()
            date = datetime.now().strftime("%d-%m-%y")
            roll_col = self.classes_data[class_name]['roll_column']
            name_col = self.classes_data[class_name]['name_column']
            
            # Update attendance for today
            attendance_list = []
            for _, row in df.iterrows():
                student_id = str(row[roll_col])
                status = 'Present' if self.attendance_records[class_name].get(student_id, False) else 'Absent'
                attendance_list.append(status)
            
            # Add today's attendance column
            df[date] = attendance_list
            
            # Identify columns that contain attendance records.
            attendance_columns = [col for col in df.columns if col not in [roll_col, name_col, "Total"]]
            
            # Recalculate the "Total" column as the count of "Present" statuses in attendance columns
            df["Total"] = df[attendance_columns].apply(lambda row: sum(1 for value in row if value == "Present"), axis=1)
            
            # Reorder columns so that "Total" always appears before any date columns
            other_columns = [col for col in df.columns if col not in [roll_col, name_col, "Total"]]
            df = df[[roll_col, name_col, "Total"] + other_columns]
            
            # Save updated DataFrame to Excel
            df.to_excel(self.classes_data[class_name]['file_path'], index=False)
            
            messagebox.showinfo("Success", "Attendance saved!")
            attendance_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")

    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceSystem()
    app.run()
