# System Architecture

## Overview
FaceTrack is a complete Biometric Attendance System utilizing modern Computer Vision practices with a lightweight web interface.

## Pipeline
The core functionality proceeds in the following sequential pipeline:

1. **Camera Feed:** Captures real-time frames from the webcam.
2. **Face Detection:** Identifies bounding boxes of faces in the frame using primarily OpenCV Haar cascades, with a fallback to HOG (Histogram of Oriented Gradients) for complex profiles.
3. **Preprocessing & Feature Extraction:** The located face crops are normalized and resized, then both HOG (structural info) and LBP (Local Binary Pattern for texture) features are extracted.
4. **KNN Classifier:** The concatenated feature vectors are fed into a K-Nearest Neighbors classifier, providing the predicted profile string and distance (confidence %).
5. **False Positive Reduction:** Employs multi-frame voting (requiring consecutive predictions) and confidence thresholds, to drastically cut down spurious matches.
6. **SQLite Database:** The verified, robust identification gets inserted into an optimized SQLite database mapping timestamps and subjects to the recognized students.
7. **Streamlit Dashboard:** The real-time live feed and analytical reporting interfaces stream the results to the user.

## Data Flow
`Streamlit (Frontend) <-> SQLite (Database) <-> Core ML Pipeline (Backend)`
