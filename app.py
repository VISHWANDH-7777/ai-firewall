from flask import Flask, render_template, jsonify, request
import threading
import time
import random
from datetime import datetime
import json
import os
from ai_model.model import ThreatDetector
import numpy as np

app = Flask(__name__)

# Initialize threat detector
detector = ThreatDetector()

# Global variables for simulation
monitoring_active = False
traffic_data = []
threat_log = []
active_attacks = {}  # Track active attacks
stats = {
    'total_packets': 0,
    'threats_detected': 0,
    'attacks_blocked': 0,
    'last_updated': datetime.now().strftime('%H:%M:%S')
}

# System health metrics
system_health = {
    'server_load': 0.3,
    'response_time': 120,
    'health_score': 100,
    'status': 'normal'
}

# AI defense status
ai_status = {
    'detection_confidence': 0.0,
    'mitigation_progress': 0.0,
    'threats_detected': 0,
    'attacks_blocked': 0
}

# Event logging
recent_events = []
event_id_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attack_monitor')
def attack_monitor():
    """Real-time attack monitoring page"""
    return render_template('attack_monitor.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global monitoring_active
    monitoring_active = True
    # Start simulation in background
    thread = threading.Thread(target=simulate_traffic)
    thread.daemon = True
    thread.start()
    
    # Start system health monitoring
    health_thread = threading.Thread(target=monitor_system_health)
    health_thread.daemon = True
    health_thread.start()
    
    # Add event
    add_event('Monitoring started', 'info')
    
    return jsonify({'status': 'monitoring_started'})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    
    # Add event
    add_event('Monitoring stopped', 'info')
    
    return jsonify({'status': 'monitoring_stopped'})

@app.route('/get_traffic_data')
def get_traffic_data():
    return jsonify({
        'traffic': traffic_data[-20:],  # Return last 20 data points
        'threats': threat_log[-10:],    # Return last 10 threats
        'stats': stats,
        'active_attacks': list(active_attacks.values())  # Send active attacks to frontend
    })

@app.route('/get_realtime_data')
def get_realtime_data():
    """Get real-time system and AI status"""
    return jsonify({
        'system_health': system_health,
        'ai_status': ai_status,
        'recent_events': recent_events[-10:]  # Last 10 events
    })

@app.route('/launch_attack', methods=['POST'])
def launch_attack():
    attack_type = request.json.get('attack_type')
    target = request.json.get('target', '192.168.1.1')
    intensity = request.json.get('intensity', 'medium')
    
    # Generate a unique ID for this attack
    attack_id = f"{attack_type}_{target}_{intensity}_{datetime.now().timestamp()}"
    
    # Store attack information
    active_attacks[attack_id] = {
        'id': attack_id,
        'type': attack_type,
        'target': target,
        'intensity': intensity,
        'start_time': datetime.now().strftime('%H:%M:%S'),
        'status': 'ongoing',
        'packets_sent': 0,
        'impact': 0.0
    }
    
    # Start attack in background thread
    thread = threading.Thread(target=run_attack_simulation, args=(attack_type, target, intensity, attack_id))
    thread.daemon = True
    thread.start()
    
    # Log the attack
    threat_log.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'type': attack_type.upper(),
        'source': 'Attack Simulator',
        'target': target,
        'severity': 'High' if intensity in ['high', 'critical'] else 'Medium',
        'attack_id': attack_id,
        'message': f'{intensity} intensity attack launched'
    })
    
    # Add event
    add_event(f'{attack_type.upper()} attack launched ({intensity} intensity)', 'threat')
    
    stats['threats_detected'] += 1
    stats['last_updated'] = datetime.now().strftime('%H:%M:%S')
    
    return jsonify({
        'status': f'{attack_type}_attack_launched',
        'attack_id': attack_id
    })

@app.route('/trigger_ai_mitigation', methods=['POST'])
def trigger_ai_mitigation():
    """Trigger AI mitigation manually"""
    global ai_status
    
    # Simulate AI mitigation
    ai_status['mitigation_progress'] = min(1.0, ai_status['mitigation_progress'] + 0.3)
    
    # Add event
    add_event('AI mitigation triggered manually', 'mitigation')
    
    # Reduce attack impact for all active attacks
    for attack_id in list(active_attacks.keys()):
        if active_attacks[attack_id]['status'] == 'ongoing':
            active_attacks[attack_id]['impact'] = max(0, active_attacks[attack_id]['impact'] * 0.5)
    
    # Update system health based on reduced impact
    update_system_health_based_on_attacks()
    
    return jsonify({'status': 'ai_mitigation_triggered'})

@app.route('/stop_attack/<attack_id>', methods=['POST'])
def stop_attack(attack_id):
    if attack_id in active_attacks:
        active_attacks[attack_id]['status'] = 'stopped'
        
        # Add event
        add_event(f'Attack {attack_id} stopped manually', 'info')
        
        return jsonify({'status': 'attack_stopped', 'attack_id': attack_id})
    return jsonify({'status': 'attack_not_found'}), 404

def add_event(message, event_type):
    """Add an event to the recent events log"""
    global recent_events, event_id_counter
    
    event_id_counter += 1
    recent_events.append({
        'id': event_id_counter,
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'message': message
    })
    
    # Keep only recent events
    if len(recent_events) > 50:
        recent_events = recent_events[-50:]

def simulate_traffic():
    """Simulate only normal network traffic (no random threats)"""
    global traffic_data, monitoring_active, stats
    
    packet_id = 0
    while monitoring_active:
        time.sleep(0.5)  # Simulate traffic every 0.5 seconds
        
        # Generate only normal traffic data (no threats)
        packet_size = random.randint(50, 1500)
        protocol = random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS'])
        source = f"192.168.1.{random.randint(1, 50)}"
        destination = f"10.0.0.{random.randint(1, 10)}"
        
        # Add to traffic data (all normal traffic)
        traffic_data.append({
            'id': packet_id,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'source': source,
            'destination': destination,
            'protocol': protocol,
            'size': packet_size,
            'threat': False,
            'threat_type': None
        })
        
        packet_id += 1
        stats['total_packets'] += 1
        stats['last_updated'] = datetime.now().strftime('%H:%M:%S')
        
        # Keep only recent data
        if len(traffic_data) > 100:
            traffic_data = traffic_data[-100:]

def run_attack_simulation(attack_type, target, intensity, attack_id):
    """Run attack simulation with realistic impact"""
    global active_attacks, stats, system_health, ai_status
    
    try:
        # Set attack parameters based on intensity
        intensity_params = {
            'low': {'duration': 15, 'packets_per_sec': 10, 'impact': 0.4},
            'medium': {'duration': 25, 'packets_per_sec': 25, 'impact': 0.6},
            'high': {'duration': 35, 'packets_per_sec': 50, 'impact': 0.8},
            'critical': {'duration': 45, 'packets_per_sec': 100, 'impact': 0.95}
        }
        
        params = intensity_params.get(intensity, intensity_params['medium'])
        
        # Simulate attack duration
        start_time = time.time()
        end_time = start_time + params['duration']
        packets_sent = 0
        
        while time.time() < end_time and active_attacks.get(attack_id, {}).get('status') == 'ongoing':
            # Calculate current impact (ramps up over time)
            elapsed = time.time() - start_time
            progress = min(1.0, elapsed / params['duration'])
            current_impact = params['impact'] * progress
            
            # Update attack impact
            if attack_id in active_attacks:
                active_attacks[attack_id]['impact'] = current_impact
                active_attacks[attack_id]['packets_sent'] = packets_sent
                active_attacks[attack_id]['progress'] = round(progress * 100, 1)
            
            # Update system health based on attack impact
            update_attack_impact(attack_type, current_impact)
            
            # Send attack packets
            packets_this_second = min(params['packets_per_sec'], int(params['packets_per_sec'] * progress))
            
            for _ in range(packets_this_second):
                if attack_type == 'ddos':
                    source_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                    traffic_data.append({
                        'id': len(traffic_data),
                        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                        'source': source_ip,
                        'destination': target,
                        'protocol': 'TCP',
                        'size': random.randint(100, 1500),
                        'threat': True,
                        'threat_type': 'DDoS',
                        'attack_id': attack_id
                    })
                elif attack_type == 'port_scan':
                    port = random.randint(20, 1000)
                    traffic_data.append({
                        'id': len(traffic_data),
                        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                        'source': f"45.33.21.{random.randint(1, 255)}",
                        'destination': f"{target}:{port}",
                        'protocol': 'TCP',
                        'size': 64,
                        'threat': True,
                        'threat_type': 'Port Scan',
                        'attack_id': attack_id
                    })
                elif attack_type == 'malware':
                    traffic_data.append({
                        'id': len(traffic_data),
                        'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                        'source': f"192.168.1.{random.randint(100, 200)}",
                        'destination': target,
                        'protocol': 'UDP',
                        'size': random.randint(500, 2000),
                        'threat': True,
                        'threat_type': 'Malware',
                        'attack_id': attack_id
                    })
                
                packets_sent += 1
                stats['total_packets'] += 1
            
            # AI Detection and Mitigation (simulated)
            if elapsed > 3:  # AI detects after 3 seconds
                detection_confidence = min(0.95, 0.7 + (elapsed / params['duration']) * 0.25)
                mitigation_progress = min(1.0, max(0, (elapsed - 3) / (params['duration'] - 5)))
                
                ai_status['detection_confidence'] = detection_confidence
                ai_status['mitigation_progress'] = mitigation_progress
                
                # Reduce impact as AI mitigates
                current_impact = params['impact'] * progress * (1 - mitigation_progress)
                update_attack_impact(attack_type, current_impact)
                
                if attack_id in active_attacks:
                    active_attacks[attack_id]['impact'] = current_impact
            
            time.sleep(1)  # Update every second
        
        # Attack completed - AI successfully mitigated
        if attack_id in active_attacks:
            active_attacks[attack_id]['status'] = 'mitigated'
            active_attacks[attack_id]['end_time'] = datetime.now().strftime('%H:%M:%S')
            active_attacks[attack_id]['mitigation_progress'] = 100
            active_attacks[attack_id]['result'] = 'AI successfully mitigated attack'
        
        stats['attacks_blocked'] += 1
        ai_status['attacks_blocked'] += 1
        
        # Add event
        add_event(f'{attack_type.upper()} attack successfully mitigated by AI', 'mitigation')
        
        # System recovery
        recover_system_health()
        
    except Exception as e:
        print(f"Attack simulation error: {e}")
        if attack_id in active_attacks:
            active_attacks[attack_id]['status'] = 'failed'
            active_attacks[attack_id]['error'] = str(e)

def update_attack_impact(attack_type, impact_level):
    """Update system health based on attack impact"""
    global system_health
    
    impact_factors = {
        'ddos': {'load': 0.8, 'response': 5.0},
        'port_scan': {'load': 0.3, 'response': 1.5},
        'malware': {'load': 0.5, 'response': 3.0}
    }
    
    factors = impact_factors.get(attack_type, {'load': 0.4, 'response': 2.0})
    
    # Apply impact
    system_health['server_load'] = min(0.95, 0.3 + (factors['load'] * impact_level))
    system_health['response_time'] = 120 + (factors['response'] * impact_level * 100)
    system_health['health_score'] = max(0, 100 - (impact_level * 70))
    
    # Update status
    if impact_level > 0.7:
        system_health['status'] = 'critical'
    elif impact_level > 0.4:
        system_health['status'] = 'degraded'
    else:
        system_health['status'] = 'normal'

def update_system_health_based_on_attacks():
    """Update system health based on all active attacks"""
    global system_health, active_attacks
    
    total_impact = 0
    for attack in active_attacks.values():
        if attack['status'] == 'ongoing':
            total_impact += attack['impact']
    
    # Normalize impact
    total_impact = min(1.0, total_impact)
    
    # Apply impact (using DDoS as baseline)
    system_health['server_load'] = min(0.95, 0.3 + (0.8 * total_impact))
    system_health['response_time'] = 120 + (5.0 * total_impact * 100)
    system_health['health_score'] = max(0, 100 - (total_impact * 70))
    
    # Update status
    if total_impact > 0.7:
        system_health['status'] = 'critical'
    elif total_impact > 0.4:
        system_health['status'] = 'degraded'
    else:
        system_health['status'] = 'normal'

def recover_system_health():
    """Gradually recover system health after attack"""
    def recovery_loop():
        for _ in range(20):  # Recovery over 20 seconds
            time.sleep(1)
            system_health['server_load'] = max(0.3, system_health['server_load'] * 0.9)
            system_health['response_time'] = max(120, system_health['response_time'] * 0.9)
            system_health['health_score'] = min(100, system_health['health_score'] + 3)
            
            if system_health['server_load'] <= 0.4:
                system_health['status'] = 'normal'
    
    threading.Thread(target=recovery_loop, daemon=True).start()

def monitor_system_health():
    """Monitor and maintain system health"""
    global system_health, monitoring_active, active_attacks
    
    while True:
        if monitoring_active:
            # Gentle normalization when no active attacks
            if not any(attack['status'] == 'ongoing' for attack in active_attacks.values()):
                system_health['server_load'] = max(0.3, min(0.5, system_health['server_load'] * 0.99))
                system_health['response_time'] = max(120, min(200, system_health['response_time'] * 0.99))
                system_health['health_score'] = min(100, system_health['health_score'] + 0.5)
            
            # Ensure values stay within bounds
            system_health['server_load'] = max(0.3, min(0.95, system_health['server_load']))
            system_health['response_time'] = max(120, min(2000, system_health['response_time']))
            system_health['health_score'] = max(0, min(100, system_health['health_score']))
        
        time.sleep(2)

# At the bottom of your app.py, replace:
if __name__ == '__main__':
    # Use environment variable for port or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run on 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=port, debug=False)