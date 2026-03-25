import sqlite3
import pandas as pd
import os

def get_recent_attendance(limit=5, db_path='facetrack.db'):
    # Path resolution based on being inside utils/
    if not os.path.exists(db_path):
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT s.name as Name, s.roll_number as 'Roll No', a.timestamp as Time, a.confidence_score as 'Conf%'
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.timestamp DESC
        LIMIT {limit}
    """
    try:
        df = pd.read_sql_query(query, conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df
