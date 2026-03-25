import streamlit as st
import cv2
import time
import numpy as np
from datetime import datetime, date
import sys
import os
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.face_detector import FaceDetector
from core.feature_extractor import FeatureExtractor
from core.face_recognizer import FaceRecognizer
from core.false_positive_reducer import FalsePositiveReducer
from database.db_handler import DBHandler
from utils.db_queries import get_recent_attendance

st.set_page_config(page_title="Live Attendance", page_icon="🎥")

st.title("Live Camera Feed - Attendance")

subject_options = ["Data Structures", "DBMS", "Machine Learning", "Operating Systems", "Computer Networks"]
selected_subject = st.sidebar.selectbox("Select Current Subject Class", subject_options)

# Initialize Core components (Cached so we don't reload models every frame)
@st.cache_resource
def load_models():
    detector = FaceDetector()
    extractor = FeatureExtractor()
    recognizer = FaceRecognizer()
    fp_reducer = FalsePositiveReducer(req_frames=3, confidence_threshold=65.0, cooldown_minutes=10)
    db = DBHandler()
    return detector, extractor, recognizer, fp_reducer, db

camera = cv2.VideoCapture(0)

detector, extractor, recognizer, fp_reducer, db = load_models()

start_camera = st.button("Start Camera Stream")
stop_camera = st.button("Stop Stream")

FRAME_WINDOW = st.image([])

# Below feed layout
st.markdown("### Real-Time Logs")
log_container = st.empty()

# Attempt to load recent
def update_logs():
    try:
        df = get_recent_attendance(limit=5)
        log_container.table(df)
    except Exception:
        pass

if "stream_active" not in st.session_state:
    st.session_state["stream_active"] = False

if start_camera:
    st.session_state.stream_active = True

if stop_camera:
    st.session_state.stream_active = False

update_logs()

if st.session_state.stream_active:
    if not camera.isOpened():
        st.error("Cannot access webcam. Showing placeholder instead if using Docker/Cloud.")
        st.session_state.stream_active = False
    
    # Process frames loop
    while st.session_state.stream_active:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to read frame.")
            break
            
        # Detect
        boxes = detector.detect(frame)
        
        # Crop & Predict
        crops = detector.crop_faces(frame, boxes)
        
        for (crop, (x, y, w, h)) in zip(crops, boxes):
            # Extract features
            fv = extractor.extract(crop)
            
            # KNN Recognize
            raw_id, conf = recognizer.predict(fv)
            
            color = (0, 0, 255) # Red for unknown
            display_name = "Unknown"
            
            # Run through False Positive Reducer
            confirmed, reason = fp_reducer.process_prediction(raw_id, conf)
            
            if confirmed:
                color = (0, 255, 0) # Green for recognized
                display_name = raw_id
                
                # Fetch student ID from DB based on Roll Number
                student = db.get_student_by_roll(raw_id)
                if student:
                    student_id = student[0] # assuming schema order
                    name = student[1] 
                    display_name = f"{name} ({raw_id})"
                    
                    # Mark Attendance
                    db.mark_attendance(
                        student_id=student_id, 
                        date=date.today().strftime('%Y-%m-%d'),
                        subject=selected_subject, 
                        confidence=conf
                    )
                    
                    st.toast(f"✅ Marked: {name}")
                    update_logs()
            else:
                if raw_id != "Unknown" and conf >= 65.0:
                    color = (255, 165, 0) # Orange if waiting for more frames
                    display_name = f"Verifying {raw_id}..."
                    
            # Draw
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{display_name} {conf:.1f}%", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
        # Convert BGR to RGB for Streamlit via PIL
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(img)
        time.sleep(0.01)

camera.release()
