import streamlit as st
import pandas as pd
import sqlite3
import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.db_handler import DBHandler

st.set_page_config(page_title="Attendance Report", layout="wide")
st.title("Attendance Report Viewer")

# Filters
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", datetime.date(2025, 1, 1))
end_date = col2.date_input("End Date", datetime.date.today())

conn = sqlite3.connect('facetrack.db')
query = f"""
    SELECT 
        s.roll_number as 'Roll Number', 
        s.name as 'Name', 
        s.department as 'Department',
        s.year as 'Year',
        a.date as 'Date', 
        a.subject as 'Subject', 
        a.timestamp as 'Time', 
        a.confidence_score as 'Confidence Score (%)'
    FROM attendance a 
    JOIN students s ON a.student_id = s.id
    WHERE a.date >= ? AND a.date <= ?
    ORDER BY a.timestamp DESC
"""
df = pd.read_sql_query(query, conn, params=(start_date, end_date))
conn.close()

if not df.empty:
    st.write(f"Found {len(df)} records.")
    
    # Highlight logic: yellow border for <70% (Borderline detection)
    def highlight_low_confidence(val):
        color = '#FFE066' if isinstance(val, (int, float)) and val < 70.0 else ''
        return f'background-color: {color}'
        
    styled_df = df.style.map(highlight_low_confidence, subset=['Confidence Score (%)'])
    
    st.dataframe(styled_df, use_container_width=True, height=600)
    
    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Export as CSV", data=csv, file_name="attendance_report.csv", mime="text/csv")
else:
    st.warning("No attendance records found for this date range. Try generating sample data.")
