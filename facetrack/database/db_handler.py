import sqlite3
import os

class DBHandler:
    """
    Handles SQLite CRUD operations for FaceTrack.
    """
    def __init__(self, db_path='facetrack.db', schema_path='database/schema.sql'):
        """
        Args:
            db_path (str): Path to SQLite DB.
            schema_path (str): Contains SQL schema to initialize the DB.
        """
        self.db_path = db_path
        self.schema_path = schema_path
        self._init_db()

    def _init_db(self):
        """Automatically initializes database strictly on the first run using schema.sql."""
        if not os.path.exists(self.db_path):
            print(f"Initializing database at {self.db_path}...")
            conn = self.get_connection()
            with open(self.schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_student(self, name, roll_number, department, year):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO students (name, roll_number, department, year, face_registered)
                VALUES (?, ?, ?, ?, 1)
            ''', (name, roll_number, department, year))
            conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError:
            print(f"Student with roll number {roll_number} already exists.")
            return None
        finally:
            conn.close()

    def mark_attendance(self, student_id, date, subject, confidence, marked_by="System"):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO attendance (student_id, date, subject, marked_by, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, date, subject, marked_by, confidence))
        conn.commit()
        conn.close()

    def get_student_by_roll(self, roll_number):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,))
        result = c.fetchone()
        conn.close()
        return result
        
    def get_student_by_id(self, student_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        result = c.fetchone()
        conn.close()
        return result
