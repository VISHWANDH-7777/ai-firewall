import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
import pandas as pd

class ThreatDetector:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'threat_detection_model.joblib')
        self.load_model()
    
    def load_model(self):
        """Load trained model if available"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("Trained model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print("No trained model found. Please train the model first.")
    
    def train_model(self, data_path):
        """Train the threat detection model"""
        try:
            # Load dataset
            print(f"Loading dataset from {data_path}...")
            data = pd.read_csv(data_path)
            
            # Check if dataset has required columns
            required_columns = [
                'packet_size', 'protocol_type', 'duration', 'source_bytes',
                'destination_bytes', 'count', 'same_srv_rate', 'serror_rate', 'threat'
            ]
            
            if not all(col in data.columns for col in required_columns):
                print("Dataset missing required columns. Regenerating dataset...")
                return False
            
            # Features and labels
            X = data[['packet_size', 'protocol_type', 'duration', 'source_bytes', 
                     'destination_bytes', 'count', 'same_srv_rate', 'serror_rate']]
            y = data['threat']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            print("Training Random Forest model...")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            print("Evaluating model...")
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Model accuracy: {accuracy:.4f}")
            
            # Show detailed report
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, target_names=['Normal', 'Threat']))
            
            # Save model
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")
            
            return True
            
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, features):
        """Predict if network traffic is a threat"""
        if self.model is None:
            print("Model not trained yet")
            return False
        
        try:
            # Convert features to numpy array and predict
            features_array = np.array(features).reshape(1, -1)
            prediction = self.model.predict(features_array)
            prediction_proba = self.model.predict_proba(features_array)
            
            print(f"Prediction confidence: {prediction_proba[0][1]:.4f}")
            return bool(prediction[0])
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return False

# For testing the model directly
if __name__ == '__main__':
    detector = ThreatDetector()
    
    # If no model exists, train one
    if detector.model is None:
        dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', 'network_traffic.csv')
        if os.path.exists(dataset_path):
            detector.train_model(dataset_path)
        else:
            print("No dataset found. Please generate data first.")