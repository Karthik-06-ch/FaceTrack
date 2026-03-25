-- Table: students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    year INTEGER NOT NULL,
    face_registered INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: subjects
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL
);

-- Table: attendance
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE NOT NULL,
    subject TEXT NOT NULL,
    marked_by TEXT DEFAULT 'System',
    confidence_score REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_student_id ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_date ON attendance(date);
