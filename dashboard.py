from flask import Flask, render_template_string
import psutil
import requests

app = Flask(__name__)

HTML_DESIGN = """
<!DOCTYPE html>
<html>
<head>
    <title>Sentinel Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding-top: 50px; }
        .card { background-color: #1e1e1e; padding: 40px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5); border: 1px solid #333; max-width: 600px; }
        h1 { color: #00bcd4; }
        .metrics-container { display: flex; justify-content: center; gap: 20px; }
        .metric-box { padding: 20px; background-color: #2c2c2c; border-radius: 10px; width: 150px; }
        .number { font-size: 36px; font-weight: bold; color: #4CAF50; }
        .ai-box { margin-top: 30px; padding: 20px; background-color: #1a2634; border-left: 5px solid #00bcd4; border-radius: 5px; text-align: left; }
        .ai-title { color: #00bcd4; font-weight: bold; margin-bottom: 10px; font-size: 18px; }
    </style>
    <meta http-equiv="refresh" content="10">
</head>
<body>
    <h1>🛡️ Sentinel AI Control Room</h1>
    <div class="card">
        <h2>Live Server Health</h2>
        
        <div class="metrics-container">
            <div class="metric-box">
                <p>CPU Usage</p>
                <div class="number">{{ cpu }}%</div>
            </div>
            <div class="metric-box">
                <p>RAM Usage</p>
                <div class="number">{{ ram }}%</div>
            </div>
        </div>

        <div class="ai-box">
            <div class="ai-title">🧠 AI System Analysis:</div>
            <div>{{ ai_message }}</div>
        </div>
        
        <p style="color: #888; font-size: 12px; margin-top:20px;">Auto-updating every 10 seconds...</p>
    </div>
</body>
</html>
"""

def get_ai_analysis(cpu, ram):
    # Notice we are using your exact Ubuntu IP address!
    url = "http://192.168.1.87:11434/api/generate"
    prompt = f"You are a DevOps AI. The server CPU is at {cpu}% and RAM is at {ram}%. In one short sentence, tell me if the system is healthy or if I should be worried."
    
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Give the AI 5 seconds to answer, otherwise show an error
        response = requests.post(url, json=payload, timeout=5)
        return response.json()['response'].strip()
    except Exception as e:
        return "⚠️ Could not connect to the AI Engine. Is Ollama running?"

@app.route('/')
def home():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    # 1. Check if the server is working hard
    if ram_usage > 40 or cpu_usage > 40:
        # Wake up the AI to analyze the spike
        ai_result = get_ai_analysis(cpu_usage, ram_usage)
    else:
        # Let the AI rest
        ai_result = "✅ System usage is very low. The AI is currently resting to save resources."

    return render_template_string(HTML_DESIGN, cpu=cpu_usage, ram=ram_usage, ai_message=ai_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
