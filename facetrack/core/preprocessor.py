import cv2
import numpy as np

class Preprocessor:
    """
    Image preprocessing functionalities: Normalization, adjustments overlay and 
    minor augmentations for robust training.
    """
    @staticmethod
    def normalize_lighting(image):
        """
        Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) 
        to mitigate uneven lighting conditions.
        
        Args:
            image (numpy.ndarray): Input BGR image.
        Returns:
            numpy.ndarray: Equalized image.
        """
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return final

    @staticmethod
    def random_augment(image):
        """
        Applies random horizontal flip or slight blurring useful as data augmentation.
        
        Args:
            image (numpy.ndarray): Cropped Face.
        Returns:
            numpy.ndarray: Augmented Image.
        """
        aug_img = image.copy()
        
        # 50% chance horizontal flip
        if np.random.rand() > 0.5:
            aug_img = cv2.flip(aug_img, 1)
            
        # 20% chance motion blur or noise
        if np.random.rand() > 0.8:
            k_size = np.random.choice([3, 5])
            aug_img = cv2.GaussianBlur(aug_img, (k_size, k_size), 0)
            
        return aug_img
