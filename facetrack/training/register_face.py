import cv2
import os
import argparse
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.face_detector import FaceDetector

def register_new_face(roll_number, num_samples=20):
    """
    Captures faces from the webcam to register a new user.
    
    Args:
        roll_number (str): Unique ID to be used as directory name.
        num_samples (int): How many images to capture.
    """
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'profiles', roll_number)
    os.makedirs(save_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    
    print(f"Starting registration for {roll_number}.")
    print("Please look at the camera. Capturing will start momentarily.")
    
    count = 0
    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access camera.")
            break
            
        # Optional: Show a guide on screen
        cv2.putText(frame, f"Capturing: {count}/{num_samples}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
        boxes = detector.detect(frame)
        
        # Only capture if exactly ONE face is in frame to avoid bad crops
        if len(boxes) == 1:
            crops = detector.crop_faces(frame, boxes)
            if crops:
                save_path = os.path.join(save_dir, f"{count}.jpg")
                cv2.imwrite(save_path, crops[0])
                count += 1
                
        # Draw boxes just for user feedback
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        cv2.imshow("Registering Face", frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Successfully saved {count} samples for {roll_number}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--roll", type=str, required=True, help="Roll number or Unique ID")
    parser.add_argument("--samples", type=int, default=20, help="Number of samples to capture")
    args = parser.parse_args()
    
    register_new_face(args.roll, args.samples)
