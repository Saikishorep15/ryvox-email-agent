import requests

BASE_URL = "http://127.0.0.1:8000"

def run():
    print("🚀 Connecting to Ryvox Email Environment...")
    
    # 1. RESET
    res = requests.post(f"{BASE_URL}/reset")
    if res.status_code != 200:
        print(f"❌ Reset Failed: {res.text}")
        return

    # Match the 'observation' key from your new app.py
    data = res.json()["observation"]
    email = "win money now!!!"
    print(f"📩 Email to classify: '{email}'")

    # 2. AGENT LOGIC
    if "win" in email or "money" in email:
        action = "spam"
    elif "meeting" in email or "urgent" in email:
        action = "important"
    else:
        action = "normal"

    print(f"🤖 Agent Action: {action}")

    # 3. STEP
    # Sending the JSON payload to match RyvoxEmailAction
    res = requests.post(f"{BASE_URL}/step", json={"action": action})
    
    if res.status_code == 200:
        result = res.json()
        print(f"✅ Step Result: Reward={result['reward']}, Done={result['done']}")
        print("🔥 TASK COMPLETE!")
    else:
        print(f"❌ Step Failed: {res.text}")

if __name__ == "__main__":
    run()