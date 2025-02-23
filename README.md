# Attendance Management System

A smartphone-oriented **Attendance Management System** built using **Python and Tkinter**, which allows users to manage student attendance records with an intuitive UI. It supports Excel file integration, automatic column detection, and data storage.

## 📌 Features
- **Class Management:** Add classes from Excel files.
- **Automatic Column Detection:** Identifies roll numbers and names automatically.
- **Attendance Tracking:** Toggle attendance with a simple tap.
- **Intelligent UI:** Alternating tile colors for better readability.
- **Excel Integration:** Saves and updates attendance records.

---

## 📂 Project Structure
```
📦 Attendance Management System
 ├── app.py  # Main script
 ├── requirements.txt  # Dependencies
 ├── README.md  # Documentation
```

---

## 🚀 How to Run
1. Install dependencies:
   ```sh
   pip install pandas tk
   ```
2. Run the script:
   ```sh
   python app.py
   ```

---

## 🛠 Components Explained

### 1️⃣ **Importing Libraries**
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime
import os
```
- **tkinter**: GUI framework for the application.
- **pandas**: Handles Excel file operations.
- **datetime**: Used to track attendance dates.
- **os**: For file handling.

### 2️⃣ **Constants for UI**
```python
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800
COLORS = { 'white': '#FFFFFF', 'black': '#2C3E50', 'absent': '#E74C3C', 'present': '#2ECC71'}
```
- Defines window dimensions and colors for UI elements.

### 3️⃣ **Initializing the Application**
```python
def __init__(self):
    self.setup_main_window()
    self.initialize_data_structures()
    self.create_main_screen()
```
- **setup_main_window()**: Creates the main application window.
- **initialize_data_structures()**: Initializes class and attendance data.
- **create_main_screen()**: Sets up the main UI layout.

### 4️⃣ **Adding a New Class**
```python
def add_new_class(self):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    df = pd.read_excel(file_path)
```
- Allows users to select an Excel file containing class data.
- Reads the data and detects roll number and name columns automatically.

### 5️⃣ **Detecting Columns Automatically**
```python
def detect_data_columns(self, df):
    roll_patterns = ['roll', 'enrollment', 'id', 'number']
    name_patterns = ['name', 'student']
```
- Searches for common keywords in column names to detect roll number and student name fields.

### 6️⃣ **Creating Class Tiles**
```python
def create_class_tile(self, class_name):
    tile = tk.Button(self.classes_frame, text=class_name, command=lambda: self.open_attendance_screen(class_name))
    tile.pack(fill=tk.X, pady=5)
```
- Adds a clickable button for each class.

### 7️⃣ **Attendance UI & Grid**
```python
def create_student_grid(self, container, class_name):
    for index, row in df.iterrows():
        button = tk.Button(frame, text=f"{student_id}\n{row[name_col]}", command=lambda sid=student_id: self.toggle_attendance(class_name, sid))
```
- Displays student names and roll numbers in a grid format.
- Allows toggling of attendance.

### 8️⃣ **Toggling Attendance Status**
```python
def toggle_attendance(self, class_name, student_id):
    current_status = self.attendance_records[class_name][student_id]
    self.attendance_records[class_name][student_id] = not current_status
```
- Changes student status from **absent** to **present** and vice versa.

### 9️⃣ **Saving Attendance Data**
```python
def save_attendance(self, class_name, attendance_window):
    df[date] = attendance_list
    df.to_excel(self.classes_data[class_name]['file_path'], index=False)
```
- Saves attendance records to the original Excel file.

---

## 📌 Future Improvements
- Export attendance reports.
- Cloud database support.
- Mobile-friendly version.

---

## 📜 License
This project is open-source. Feel free to modify and improve it!

---
