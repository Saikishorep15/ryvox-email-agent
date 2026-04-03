import os
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction
from openai import OpenAI

# 🔑 ENV VARIABLES (MANDATORY)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL
)

env = RyvoxEmailEnvironment()


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


def fallback_action(email):
    email = email.lower()

    if "win" in email or "money" in email or "offer" in email:
        return "spam"
    elif "meeting" in email or "discuss" in email or "project" in email:
        return "important"
    else:
        return "normal"


def run():
    print("[START] Evaluation Started")

    total_reward = 0
    episodes = 5

    for i in range(episodes):
        print(f"[STEP] Episode {i+1}")

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

    final_score = total_reward / episodes

    print(f"[END] Final Score: {round(final_score, 2)}")


if __name__ == "__main__":
    run()