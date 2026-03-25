import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd
import os
from .db_handler import DBHandler

def generate_synthetic_data(db_path='facetrack.db', csv_out='data/sample_attendance.csv'):
    """
    Generates 200+ unique student profiles and 500+ realistic attendance records.
    Outputs to both SQLite and CSV.
    """
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Needs a db_handler initialized to create the schema!
    # Because we're in database/, we ensure paths are relative correctly.
    # Assume script is run from project root.
    db = DBHandler(db_path=db_path)
    conn = db.get_connection()
    c = conn.cursor()
    
    departments = ['Computer Science', 'Information Technology', 'Electronics', 'Mechanical']
    subjects = ['Data Structures', 'DBMS', 'Machine Learning', 'Operating Systems', 'Computer Networks']
    
    # Insert Subjects
    for idx, sub in enumerate(subjects):
        c.execute("INSERT OR IGNORE INTO subjects (name, code, department) VALUES (?, ?, ?)", 
                  (sub, f"C{idx+101}", random.choice(departments)))
    
    # 1. Generate 200+ Students
    student_ids = []
    for i in range(1, 210):
        name = f"Student_{i}"
        roll = f"CS2025{i:03d}"
        dept = random.choice(departments)
        year = random.choice([1, 2, 3, 4])
        
        c.execute('''
            INSERT INTO students (name, roll_number, department, year, face_registered)
            VALUES (?, ?, ?, ?, 1)
        ''', (name, roll, dept, year))
        student_ids.append(c.lastrowid)
    
    # 2. Generate 500+ Attendance Records spanning Jan to Mar 2025
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 31)
    days_diff = (end_date - start_date).days
    
    attendance_records = []
    
    for _ in range(550): # 500+ rows
        student_id = random.choice(student_ids)
        random_day = start_date + timedelta(days=random.randint(0, days_diff))
        date_str = random_day.strftime('%Y-%m-%d')
        time_str = random_day.strftime('%Y-%m-%d 09:%M:%S')
        sub = random.choice(subjects)
        
        # Determine confidence score (62.0 to 99.0)
        # Include ~5% unknown/rejected entries
        if random.random() < 0.05:
            conf = round(random.uniform(30.0, 59.0), 1)
            marked = 'Manual'
        else:
            conf = round(random.uniform(62.0, 99.0), 1)
            marked = 'System'
            
        c.execute('''
            INSERT INTO attendance (student_id, timestamp, date, subject, marked_by, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, time_str, date_str, sub, marked, conf))
        
        attendance_records.append({
            'student_id': student_id,
            'timestamp': time_str,
            'date': date_str,
            'subject': sub,
            'marked_by': marked,
            'confidence_score': conf
        })
        
    conn.commit()
    conn.close()
    
    # Dump to CSV
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(attendance_records)
    df.to_csv(csv_out, index=False)
    print(f"Successfully generated {len(student_ids)} students and {len(attendance_records)} attendance records.")

if __name__ == "__main__":
    # If run standalone
    generate_synthetic_data()
