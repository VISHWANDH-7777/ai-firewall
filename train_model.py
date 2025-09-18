import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_model.model import ThreatDetector

def main():
    print("Training AI threat detection model...")
    
    # Initialize threat detector
    detector = ThreatDetector()
    
    # Check if dataset exists
    dataset_path = 'ai_model/datasets/network_traffic.csv'
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        print("Please generate the dataset first:")
        print("python ai_model/datasets/generate_data.py")
        return
    
    # Train model with generated dataset
    print("Loading dataset...")
    detector.train_model(dataset_path)
    
    # Test with sample data
    print("Testing with sample data...")
    sample_features = [500, 2, 0.5, 1000, 2000, 10, 0.8, 0.1]
    prediction = detector.predict(sample_features)
    print(f"Sample prediction: {'THREAT' if prediction else 'NORMAL'}")
    
    print("Model training completed successfully!")

if __name__ == '__main__':
    main()