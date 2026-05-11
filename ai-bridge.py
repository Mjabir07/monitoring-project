from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# The address of your local AI brain
OLLAMA_URL = "http://192.168.1.87:11434/api/generate"

@app.route('/alert', methods=['POST'])
def handle_alert():
    data = request.json
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚨 INCOMING ALERT FROM GRAFANA 🚨")
    
    status = data.get('status', 'unknown')
    alerts = data.get('alerts', [])
    
    if not alerts:
        return jsonify({"status": "ignored", "reason": "No alert data found"}), 200
        
    for alert in alerts:
        # Extract the specific details Grafana sent us
        alert_name = alert.get('labels', {}).get('alertname', 'Unknown Anomaly')
        server = alert.get('labels', {}).get('instance', 'Unknown Server')
        description = alert.get('annotations', {}).get('description', 'No specific description.')
        
        # Build the dynamic prompt for Phi-3
        prompt = (f"You are a Lead Cloud & System Administrator AI named Sentinel. "
                  f"A server alert named '{alert_name}' has triggered on the server '{server}'. "
                  f"The current status is {status.upper()}. Details from Prometheus: {description}. "
                  f"Write a short, professional, 3-sentence incident report explaining what this means to a CTO, "
                  f"and suggest one quick troubleshooting step.")
        
        print(f"🧠 Waking up Phi-3 AI to analyze '{alert_name}' on {server}...")
        
        payload = {
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Send the data to the AI and wait for the response
            response = requests.post(OLLAMA_URL, json=payload, timeout=45)
            ai_text = response.json().get('response', '').strip()
            
            # Print the final report to the console
            print("\n" + "="*60)
            print("📑 SENTINEL AI INCIDENT REPORT")
            print("="*60)
            print(ai_text)
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"⚠️ Failed to connect to local AI Engine: {e}")
            
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Listen on port 5001 so it doesn't conflict with Grafana
    app.run(host='0.0.0.0', port=5001)
