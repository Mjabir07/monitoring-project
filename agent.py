import psutil
import time
import datetime
import requests # The new "Waiter" library
import json

# 1. The AI Connection Function
def ask_ai_for_analysis(cpu, ram):
    # This is the local address where Ollama is listening
    url = "http://localhost:11434/api/generate"
    
    # We write a prompt, just like ChatGPT, but injecting our real-time data
    prompt = f"You are a DevOps AI. The server CPU is at {cpu}% and RAM is at {ram}%. In one short sentence, tell me if the system is healthy or if I should be worried."
    
    # We package the message for Ollama
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Send the data to the AI
        response = requests.post(url, json=payload)
        ai_answer = response.json()['response']
        print(f"  🧠 AI Detective: {ai_answer.strip()}")
    except Exception as e:
        print("  ⚠️ Error: Could not reach the AI Brain.")

# 2. The Main Monitoring Loop
def monitor_system():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    print(f"\n[{now}] Sentinel Report:")
    print(f"  > CPU Usage: {cpu_usage}%")
    print(f"  > RAM Usage: {ram_usage}%")
    
    # If the server is working hard, wake up the AI to analyze it
    if ram_usage > 50 or cpu_usage > 50:
        print("  🚨 High usage detected! Asking AI for analysis...")
        ask_ai_for_analysis(cpu_usage, ram_usage)
    else:
        print("  ✅ System is resting. No AI analysis needed right now.")

if __name__ == "__main__":
    print("Sentinel Agent is starting with AI Integration...")
    while True:
        monitor_system()
        time.sleep(10) # We wait 10 seconds so we don't spam the AI
