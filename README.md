# AI-Powered Virtual Firewall with Self-Healing

This project implements a virtual firewall with AI-powered threat detection and a web-based management interface.

## Features

- Real-time network traffic monitoring
- AI-based threat detection using machine learning
- Beautiful web dashboard for visualization
- Manual attack simulation capabilities
- Self-healing capabilities for automatic threat mitigation

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Generate training data: `python ai_model/datasets/generate_data.py`
4. Train the AI model: `python ai_model/train_model.py`
5. Run the application: `python app.py`
6. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Use the dashboard to monitor network traffic in real-time
2. Click "Start Monitoring" to begin analyzing traffic
3. Use the "Launch Attack" section to simulate various network attacks
4. View detection results and system responses in the dashboard

## Project Structure

- `app.py` - Main Flask application
- `ai_model/` - AI model training and inference code
- `attacks/` - Network attack simulation scripts
- `static/` - CSS and JavaScript files
- `templates/` - HTML templates

## Note

This is a simulation environment for educational purposes. Some attack simulations may require administrator privileges or specific network configurations.