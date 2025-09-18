import pandas as pd
import numpy as np
import random
import os

def generate_dataset(num_samples=10000):
    """Generate synthetic network traffic data for training"""
    print(f"Generating {num_samples} network traffic samples...")
    
    data = []
    
    for i in range(num_samples):
        # Generate normal traffic (80% of samples)
        if random.random() < 0.8:
            packet_size = random.randint(40, 1500)
            protocol_type = random.randint(0, 3)  # 0: TCP, 1: UDP, 2: ICMP, 3: Other
            duration = random.uniform(0, 1.0)
            source_bytes = random.randint(0, 5000)
            destination_bytes = random.randint(0, 5000)
            count = random.randint(1, 10)
            same_srv_rate = random.uniform(0.7, 1.0)
            serror_rate = random.uniform(0.0, 0.1)
            threat = 0  # Normal traffic
            
        # Generate threat traffic (20% of samples)
        else:
            packet_size = random.randint(1000, 2000) if random.random() < 0.5 else random.randint(40, 100)
            protocol_type = random.randint(0, 3)
            duration = random.uniform(0.5, 5.0) if random.random() < 0.3 else random.uniform(0, 0.5)
            source_bytes = random.randint(5000, 10000) if random.random() < 0.5 else random.randint(0, 100)
            destination_bytes = random.randint(5000, 10000) if random.random() < 0.5 else random.randint(0, 100)
            count = random.randint(10, 100) if random.random() < 0.6 else random.randint(1, 10)
            same_srv_rate = random.uniform(0.0, 0.3) if random.random() < 0.7 else random.uniform(0.3, 0.7)
            serror_rate = random.uniform(0.3, 1.0)
            threat = 1  # Threat traffic
        
        data.append([
            packet_size, protocol_type, duration, source_bytes,
            destination_bytes, count, same_srv_rate, serror_rate, threat
        ])
    
    # Create DataFrame
    columns = [
        'packet_size', 'protocol_type', 'duration', 'source_bytes',
        'destination_bytes', 'count', 'same_srv_rate', 'serror_rate', 'threat'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    # Create datasets directory if it doesn't exist
    os.makedirs(os.path.dirname('ai_model/datasets/'), exist_ok=True)
    
    # Save to CSV
    file_path = 'ai_model/datasets/network_traffic.csv'
    df.to_csv(file_path, index=False)
    print(f"Generated {num_samples} samples and saved to {file_path}")
    
    # Show dataset statistics
    normal_count = len(df[df['threat'] == 0])
    threat_count = len(df[df['threat'] == 1])
    print(f"Normal traffic: {normal_count} samples")
    print(f"Threat traffic: {threat_count} samples")
    print(f"Threat percentage: {(threat_count/num_samples)*100:.2f}%")

def generate_attack_samples(num_samples=1000, attack_type='ddos'):
    """Generate specific attack type samples"""
    print(f"Generating {num_samples} {attack_type.upper()} attack samples...")
    
    data = []
    
    for i in range(num_samples):
        if attack_type == 'ddos':
            packet_size = random.randint(1000, 2000)
            protocol_type = 0  # TCP
            duration = random.uniform(0.1, 0.5)
            source_bytes = random.randint(5000, 15000)
            destination_bytes = random.randint(100, 500)
            count = random.randint(50, 200)
            same_srv_rate = random.uniform(0.0, 0.2)
            serror_rate = random.uniform(0.8, 1.0)
            
        elif attack_type == 'port_scan':
            packet_size = random.randint(40, 100)
            protocol_type = 0  # TCP
            duration = random.uniform(0.01, 0.1)
            source_bytes = random.randint(0, 100)
            destination_bytes = random.randint(0, 100)
            count = random.randint(20, 100)
            same_srv_rate = random.uniform(0.1, 0.4)
            serror_rate = random.uniform(0.6, 0.9)
            
        elif attack_type == 'malware':
            packet_size = random.randint(500, 1500)
            protocol_type = random.choice([0, 1])  # TCP or UDP
            duration = random.uniform(1.0, 10.0)
            source_bytes = random.randint(1000, 5000)
            destination_bytes = random.randint(1000, 5000)
            count = random.randint(5, 20)
            same_srv_rate = random.uniform(0.3, 0.7)
            serror_rate = random.uniform(0.4, 0.8)
            
        else:
            # Generic threat
            packet_size = random.randint(1000, 2000) if random.random() < 0.5 else random.randint(40, 100)
            protocol_type = random.randint(0, 3)
            duration = random.uniform(0.5, 5.0) if random.random() < 0.3 else random.uniform(0, 0.5)
            source_bytes = random.randint(5000, 10000) if random.random() < 0.5 else random.randint(0, 100)
            destination_bytes = random.randint(5000, 10000) if random.random() < 0.5 else random.randint(0, 100)
            count = random.randint(10, 100) if random.random() < 0.6 else random.randint(1, 10)
            same_srv_rate = random.uniform(0.0, 0.3) if random.random() < 0.7 else random.uniform(0.3, 0.7)
            serror_rate = random.uniform(0.3, 1.0)
        
        data.append([
            packet_size, protocol_type, duration, source_bytes,
            destination_bytes, count, same_srv_rate, serror_rate, 1  # threat=1
        ])
    
    return data

def generate_comprehensive_dataset(num_samples=15000):
    """Generate a comprehensive dataset with different attack types"""
    print(f"Generating comprehensive dataset with {num_samples} samples...")
    
    # 70% normal traffic
    normal_samples = int(num_samples * 0.7)
    # 30% attack traffic (10% each of 3 attack types)
    attack_samples_per_type = int(num_samples * 0.1)
    
    data = []
    
    # Generate normal traffic
    print("Generating normal traffic samples...")
    for i in range(normal_samples):
        packet_size = random.randint(40, 1500)
        protocol_type = random.randint(0, 3)
        duration = random.uniform(0, 1.0)
        source_bytes = random.randint(0, 5000)
        destination_bytes = random.randint(0, 5000)
        count = random.randint(1, 10)
        same_srv_rate = random.uniform(0.7, 1.0)
        serror_rate = random.uniform(0.0, 0.1)
        threat = 0
        
        data.append([
            packet_size, protocol_type, duration, source_bytes,
            destination_bytes, count, same_srv_rate, serror_rate, threat
        ])
    
    # Generate different attack types
    attack_types = ['ddos', 'port_scan', 'malware']
    for attack_type in attack_types:
        print(f"Generating {attack_type} attack samples...")
        attack_data = generate_attack_samples(attack_samples_per_type, attack_type)
        data.extend(attack_data)
    
    # Shuffle the data
    random.shuffle(data)
    
    # Create DataFrame
    columns = [
        'packet_size', 'protocol_type', 'duration', 'source_bytes',
        'destination_bytes', 'count', 'same_srv_rate', 'serror_rate', 'threat'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    # Create datasets directory if it doesn't exist
    os.makedirs(os.path.dirname('ai_model/datasets/'), exist_ok=True)
    
    # Save to CSV
    file_path = 'ai_model/datasets/network_traffic.csv'
    df.to_csv(file_path, index=False)
    print(f"Generated comprehensive dataset with {len(data)} samples")
    print(f"Saved to {file_path}")
    
    # Show dataset statistics
    normal_count = len(df[df['threat'] == 0])
    threat_count = len(df[df['threat'] == 1])
    
    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Normal traffic: {normal_count} samples ({normal_count/len(df)*100:.2f}%)")
    print(f"Threat traffic: {threat_count} samples ({threat_count/len(df)*100:.2f}%)")
    
    # Show attack type distribution
    if threat_count > 0:
        print(f"\nAttack Type Distribution:")
        # You could add attack type labels to get more detailed statistics
    
    return df

if __name__ == '__main__':
    # Generate basic dataset
    generate_dataset(10000)
    
    # Alternatively, generate comprehensive dataset
    # generate_comprehensive_dataset(15000)
    
    print("\nDataset generation completed!")
    print("\nNext steps:")
    print("1. Train the AI model: python -m ai_model.train_model")
    print("2. Start the firewall: python app.py")