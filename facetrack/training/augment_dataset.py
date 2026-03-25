import os
import cv2
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.preprocessor import Preprocessor

def augment_existing_profiles():
    """
    Iterates through dataset and applies augmentation (flip/blur) 
    to multiply dataset size artificially for better KNN robustness.
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'profiles')
    
    if not os.path.exists(data_dir):
        return
        
    for user_name in os.listdir(data_dir):
        user_dir = os.path.join(data_dir, user_name)
        if not os.path.isdir(user_dir):
            continue
            
        print(f"Augmenting {user_name}...")
        for img_name in os.listdir(user_dir):
            # Skip already augmented
            if img_name.startswith('aug_'):
                continue
                
            img_path = os.path.join(user_dir, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                # Apply custom random augmentation
                aug1 = Preprocessor.random_augment(img)
                aug2 = Preprocessor.random_augment(cv2.flip(img, 1)) # Explicit flip
                
                cv2.imwrite(os.path.join(user_dir, f"aug_1_{img_name}"), aug1)
                cv2.imwrite(os.path.join(user_dir, f"aug_2_{img_name}"), aug2)

if __name__ == "__main__":
    augment_existing_profiles()
