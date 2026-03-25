import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_handler import DBHandler

# Must be the first Streamlit command
st.set_page_config(
    page_title="FaceTrack - Biometric Attendance",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Force a clean dark sidebar and neat main area 
# Using Streamlit's native custom CSS injection
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #111827;
            color: white;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
            color: #E5E7EB;
        }
        .main {
            background-color: #FAFAFA;
        }
    </style>
""", unsafe_allow_html=True)

def initialize_database():
    # Will safely init if it doesn't exist
    DBHandler(db_path='facetrack.db', schema_path='database/schema.sql')

def fetch_kpis():
    conn = sqlite3.connect('facetrack.db')
    c = conn.cursor()
    
    # Total Students
    c.execute("SELECT COUNT(*) FROM students")
    total_students = c.fetchone()[0]
    
    # Today's marked attendance
    today = date.today().strftime('%Y-%m-%d')
    c.execute("SELECT COUNT(DISTINCT student_id) FROM attendance WHERE date = ?", (today,))
    today_marked = c.fetchone()[0]
    
    conn.close()
    
    # Calculate attendance %
    attendance_pct = 0
    if total_students > 0:
        attendance_pct = round((today_marked / total_students) * 100, 1)
        
    return total_students, today_marked, attendance_pct

def main():
    initialize_database()
    
    st.title("FaceTrack Dashboard")
    st.markdown("Automated Biometric Attendance System powered by Computer Vision.")
    
    try:
        total_students, today_marked, att_pct = fetch_kpis()
    except Exception as e:
        total_students, today_marked, att_pct = 0, 0, 0
        st.warning(f"Could not load KPIs: Run python -m database.seed_data. Error: {e}")
        
    st.markdown("### Daily Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Registered Students", total_students, delta="All Time")
    col2.metric("Today's Attendees", today_marked, delta="+ Live")
    col3.metric("Live Attendance %", f"{att_pct}%", delta=None, delta_color="normal")
    
    st.write("---")
    st.markdown("#### Please select an action from the sidebar navigation to get started.")
    
if __name__ == "__main__":
    main()
