import cv2
import numpy as np

class FaceDetector:
    """
    Handles face detection utilizing OpenCV Haar Cascades and HOG as a fallback.
    Ensures minimum face sizes and bounds checking.
    """
    def __init__(self, min_size=(60, 60)):
        """
        Initializes the primary Haar classifier and the HOG fallback.
        
        Args:
            min_size (tuple): Minimum 60x60 width/height of standard faces to ignore distant noise.
        """
        self.min_size = min_size
        self.haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.hog_detector = cv2.HOGDescriptor()
        self.hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame):
        """
        Detects faces in a given frame. Returns bounding boxes.
        
        Args:
            frame (numpy.ndarray): The BGR frame as provided by OpenCV.
            
        Returns:
            list: List of tuples (x, y, w, h) indicating the bounding boxes.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Primary: Haar Cascade
        faces = self.haar_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Returns coordinates. Since Haar cascade does not provide direct confidence reliably, 
        # we treat Haar detection as foundational boxes.
        return list(faces)

    def crop_faces(self, frame, bounding_boxes):
        """
        Generates face crops based on bounding boxes.
        
        Args:
            frame (numpy.ndarray): Original frame.
            bounding_boxes (list): List of (x,y,w,h).
             
        Returns:
            list: Extracted cropped face RGB images.
        """
        crops = []
        for (x, y, w, h) in bounding_boxes:
            # Add small padding
            pad_x = int(w * 0.1)
            pad_y = int(h * 0.1)
            
            y_start = max(0, y - pad_y)
            y_end = min(frame.shape[0], y + h + pad_y)
            x_start = max(0, x - pad_x)
            x_end = min(frame.shape[1], x + w + pad_x)
            
            crop = frame[y_start:y_end, x_start:x_end]
            if crop.size > 0:
                crops.append(crop)
        return crops
