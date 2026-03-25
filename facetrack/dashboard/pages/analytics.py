import streamlit as st
import sys
import os
import sqlite3
import pandas as pd
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.chart_helpers import plot_attendance_trend, plot_subject_attendance, plot_present_absent_pie

st.set_page_config(page_title="Analytics Dashboard", layout="wide")
st.title("Attendance Analytics")

# Load data locally for charting
@st.cache_data
def get_analytics_data():
    conn = sqlite3.connect('facetrack.db')
    
    # 30-day trend
    end = datetime.date.today()
    start = end - datetime.timedelta(days=30)
    
    trend_df = pd.read_sql_query('''
        SELECT date, count(distinct student_id) as attendees 
        FROM attendance 
        WHERE date >= ? 
        GROUP BY date
    ''', conn, params=(start,))
    
    # Subject breakdown
    subject_df = pd.read_sql_query('''
        SELECT subject, count(*) as count 
        FROM attendance 
        GROUP BY subject
    ''', conn)
    
    # Top 5 absent
    # Absenteeism is complex in synthetic DB without schedules, 
    # we approximate by those with lowest total counts.
    absent_df = pd.read_sql_query('''
        SELECT s.name, s.roll_number, COUNT(a.id) as classes_attended
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id
        ORDER BY classes_attended ASC
        LIMIT 5
    ''', conn)
    
    # Simple ratio: 200 total students * 30 days = 6000 possible class-days
    # Compare to actual total
    total_att_rows = pd.read_sql_query('SELECT COUNT(*) FROM attendance', conn).iloc[0,0]
    total_stu = pd.read_sql_query('SELECT COUNT(*) FROM students', conn).iloc[0,0]
    
    conn.close()
    return trend_df, subject_df, absent_df, total_att_rows, total_stu

try:
    trend_df, subject_df, absent_df, total_att_rows, total_stu = get_analytics_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_attendance_trend(trend_df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_subject_attendance(subject_df), use_container_width=True)
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        # Mocking generic metric: Assumed ~30 classes per student total
        max_possible = total_stu * 30
        if max_possible == 0:
            max_possible = 1
        st.plotly_chart(plot_present_absent_pie(total_att_rows, max_possible - total_att_rows), use_container_width=True)
        
    with col4:
        st.subheader("Top 5 Students Needing Attention (Lowest Attendance)")
        st.table(absent_df)
        
except Exception as e:
    st.error(f"Cannot load analytics. Ensure database has data.")
    st.code(e)
