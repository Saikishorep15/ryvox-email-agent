import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_URL = "http://127.0.0.1:8000"


def get_ai_action(email):
    prompt = f"""
Classify the following email into one of these categories:
spam, important, normal

Email:
{email}

Answer ONLY one word: spam / important / normal
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()


def fallback_action(email):
    email = email.lower()

    if "win" in email or "money" in email or "offer" in email:
        return "spam"
    elif "meeting" in email or "discuss" in email or "project" in email:
        return "important"
    else:
        return "normal"


def run():
    print("🚀 Connecting to Ryvox Email Environment...")

    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()["observation"]

    email = data["email_text"]
    print(f"📩 Email: {email}")

    if os.getenv("OPENAI_API_KEY"):
        try:
            print("🤖 Using OpenAI Agent...")
            action = get_ai_action(email)
        except:
            print("⚠️ OpenAI failed, using fallback")
            action = fallback_action(email)
    else:
        print("⚠️ No API key, using fallback")
        action = fallback_action(email)

    print(f"🤖 Action: {action}")

    res = requests.post(f"{BASE_URL}/step", json={"action": action})
    result = res.json()

    print(f"✅ Reward: {result['reward']} | Done: {result['done']}")

    if result["done"]:
        print("🔥 Task Complete")


if __name__ == "__main__":
    run()