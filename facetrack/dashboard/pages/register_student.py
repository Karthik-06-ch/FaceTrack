import streamlit as st
import sys
import os
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.db_handler import DBHandler

st.title("Register New Student")

db = DBHandler()

with st.form("register_form"):
    st.subheader("Student Details")
    name = st.text_input("Full Name")
    roll_number = st.text_input("Roll Number / Identifier")
    department = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical"])
    year = st.selectbox("Year", [1, 2, 3, 4])
    
    submit_details = st.form_submit_button("1. Save to Database")
    
if submit_details:
    if name and roll_number:
        result = db.add_student(name, roll_number, department, year)
        if result:
            st.success(f"Student {name} registered in DB.")
            st.session_state['ready_to_capture'] = roll_number
        else:
            st.error("Roll number already exists in DB!")
    else:
        st.warning("Please fill required fields.")

if 'ready_to_capture' in st.session_state:
    st.info("Step 2: Start Camera to capture 20 facial samples.")
    
    if st.button("2. Launch Camera Capture UI"):
        roll = st.session_state['ready_to_capture']
        st.write("Launching OpenCV window in a separate Python process...")
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'training', 'register_face.py')
        
        # Run externally since streamlit and cv2.imshow block each other sometimes
        subprocess.Popen(["python", script_path, "--roll", roll])
        st.success("Please look at the popup window!")
        
    if st.button("3. Retrain Pipeline"):
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'training', 'train_knn.py')
        subprocess.run(["python", script_path])
        st.success("Re-Training Complete! Model Pickled.")
