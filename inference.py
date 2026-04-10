import os
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

env = RyvoxEmailEnvironment()


def fallback_action(email):
    email = email.lower()

    spam_keywords = [
        "win", "money", "offer", "bet", "betting", "gambling",
        "casino", "lottery", "prize", "free", "bonus",
        "click", "urgent", "limited", "exclusive",
        "credit", "loan", "investment", "earn",
        "guaranteed", "risk-free", "profit"
    ]

    important_keywords = [
        "meeting", "project", "report", "discussion",
        "deadline", "client", "schedule", "review"
    ]

    spam_score = sum(email.count(word) for word in spam_keywords)
    important_score = sum(email.count(word) for word in important_keywords)

    length_factor = max(1, len(email.split()) / 50)

    spam_score = spam_score / length_factor
    important_score = important_score / length_factor

    if spam_score >= 1:
        return "spam"
    elif important_score >= 0.5:
        return "important"
    else:
        return "normal"


def get_ai_action(email):
    prompt = f"""
Classify the email into: spam, important, normal.

Email:
{email}

Answer ONLY one word.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()


def run():
    print("[START] Evaluation Started")

    total_reward = 0

    # 🔥 FORCE ALL 3 TASKS (VERY IMPORTANT)
    for i in range(3):
        print(f"[STEP] Task {i+1}")

        obs = env.reset()
        email = obs.email_text

        print(f"[STEP] Email: {email}")

        try:
            action_value = get_ai_action(email)
        except:
            action_value = fallback_action(email)

        print(f"[STEP] Action: {action_value}")

        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        print(f"[STEP] Reward: {reward}")

        total_reward += reward

    # 🔥 EXTRA RUNS (OPTIONAL BUT SAFE)
    for i in range(2):
        obs = env.reset()
        email = obs.email_text

        try:
            action_value = get_ai_action(email)
        except:
            action_value = fallback_action(email)

        action = RyvoxEmailAction(action=action_value)
        obs, reward, done, _ = env.step(action)

        total_reward += reward

    final_score = total_reward / 5

    print(f"[END] Final Score: {round(final_score, 2)}")

if __name__ == "__main__":
    run()