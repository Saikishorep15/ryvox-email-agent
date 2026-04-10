import os
from openai import OpenAI
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

# 🔥 MUST use provided env variables (VERY IMPORTANT)
client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"]
)

MODEL_NAME = os.environ["MODEL_NAME"]

env = RyvoxEmailEnvironment()


def get_ai_action(email):
    prompt = f"""
Classify this email into: spam, important, normal.

Email:
{email}

Answer ONLY one word.
"""

    # 🔥 MUST call API (NO try/except, NO fallback)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()


def run():
    rewards = []
    steps = 0

    # ✅ REQUIRED FORMAT
    print(f"[START] task=ryvox env=email model={MODEL_NAME}")

    for i in range(3):  # 🔥 EXACTLY 3 TASKS
        obs = env.reset()
        email = obs.email_text

        action_value = get_ai_action(email)
        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        steps += 1
        rewards.append(reward)

        # ✅ REQUIRED STEP FORMAT
        print(f"[STEP] step={steps} action={action_value} reward={reward:.2f} done=true error=null")

    score = sum(rewards) / len(rewards)
    success = score > 0.1

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    # ✅ REQUIRED END FORMAT
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run()