import pickle
import numpy as np
import os

class FaceRecognizer:
    """
    KNN-based face recognition pipeline mapping features to identities.
    """
    def __init__(self, model_path='models/knn_model.pkl', label_path='models/label_encoder.pkl', threshold=60.0):
        """
        Initializes the model, attempting to load artifacts.
        
        Args:
            model_path (str): Path to saved `.pkl` KNN model.
            label_path (str): Path to saved `.pkl` LabelEncoder.
            threshold (float): Minimum confidence %. Below this, it is "Unknown".
        """
        self.model_path = model_path
        self.label_path = label_path
        self.threshold = threshold
        
        self.model = None
        self.le = None
        
        self._load_model()

    def _load_model(self):
        """Internal helper to load pickled models safely"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.label_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.label_path, 'rb') as f:
                    self.le = pickle.load(f)
        except Exception as e:
            print(f"Failed to load KNN model: {e}")

    def is_loaded(self):
        """Check if model is successfully loaded."""
        return self.model is not None and self.le is not None

    def predict(self, feature_vector):
        """
        Predict identity given a feature vector.
        
        Args:
            feature_vector (numpy.ndarray): 1D array from FeatureExtractor.
            
        Returns:
            tuple: (Predicted Name/ID string, Confidence Score out of 100)
        """
        if not self.is_loaded():
            return "Unknown", 0.0

        feat = feature_vector.reshape(1, -1)
        
        # Get distances and indices of nearest neighbors
        distances, indices = self.model.kneighbors(feat, n_neighbors=5)
        
        # Scikit-learn KNN distances with Euclidean metric
        # Convert distance to confidence %
        mean_dist = np.mean(distances[0])
        
        # The smaller the distance, the higher confidence (heuristic conversion)
        # Distance ~0 = 100%, Distance ~1.5 = ~0%
        # max distance depends on features, L2 norm limits it usually near 1.414 (sqrt(2))
        confidence = max(0.0, min(100.0, (1.0 - (mean_dist / 1.5)) * 100.0))
        
        # If we are too far from the cluster (threshold filter)
        if confidence < self.threshold:
            return "Unknown", confidence
            
        # Actual prediction class
        pred_idx = self.model.predict(feat)[0]
        label = self.le.inverse_transform([pred_idx])[0]
        
        return label, confidence

    def predict_batch(self, feature_vectors):
        """
        Predicts across a batch of features efficiently.
        
        Args:
            feature_vectors (list[numpy.ndarray]): List of 1D arrays.
            
        Returns:
            list: List of (label, confidence) tuples.
        """
        return [self.predict(fv) for fv in feature_vectors]
