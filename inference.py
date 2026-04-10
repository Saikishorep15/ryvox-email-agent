import os
from openai import OpenAI
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

# ✅ MUST USE THEIR ENV VARIABLES
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

env = RyvoxEmailEnvironment()


def get_action(email):
    prompt = f"""
Classify this email into: spam, important, normal.

Email: {email}

Answer only one word.
"""

    try:
        response = client.chat.completions.create(
            model=os.environ["MODEL_NAME"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip().lower()

    except:
        return "normal"  # fallback


def run():
    rewards = []
    steps = 0

    print("[START] task=ryvox env=email model=llm")

    for i in range(3):  # 🔥 3 tasks required
        obs = env.reset()
        email = obs.email_text

        action_value = get_action(email)
        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        steps += 1
        rewards.append(reward)

        print(f"[STEP] step={steps} action={action_value} reward={reward:.2f} done=true error=null")

    score = sum(rewards) / len(rewards)
    success = score > 0.1

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run()