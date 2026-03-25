import cv2
import numpy as np
from skimage.feature import hog
from skimage.feature import local_binary_pattern

class FeatureExtractor:
    """
    Extracts high-quality features from detected faces:
    Combines Histogram of Oriented Gradients (HOG) and Local Binary Pattern (LBP).
    """
    def __init__(self, target_size=(128, 128)):
        """
        Args:
            target_size (tuple): All crops are resized to this before extraction.
        """
        self.target_size = target_size
        self.lbp_radius = 1
        self.lbp_n_points = 8 * self.lbp_radius

    def extract(self, image):
        """
        Extract features from a cropped face image.
        
        Args:
            image (numpy.ndarray): Cropped BGR face image.
            
        Returns:
            numpy.ndarray: Normalized 1D feature array (HOG + LBP).
        """
        # Resize all to 128x128
        resized = cv2.resize(image, self.target_size)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # 1. HOG Extraction for structure
        hog_features = hog(
            gray, 
            orientations=9, 
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2), 
            block_norm='L2-Hys', 
            feature_vector=True
        )
        
        # 2. LBP for texture representation
        lbp = local_binary_pattern(gray, self.lbp_n_points, self.lbp_radius, method='uniform')
        (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, self.lbp_n_points + 3), range=(0, self.lbp_n_points + 2))
        
        # Normalize LBP histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)
        
        # 3. Concatenate Features
        combined_features = np.hstack([hog_features, hist])
        
        # Final Normalization for the combined vector
        norm = np.linalg.norm(combined_features)
        if norm > 0:
            combined_features = combined_features / norm
            
        return combined_features
