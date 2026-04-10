import os
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction
from openai import OpenAI

# ✅ USE PROVIDED VARIABLES (VERY IMPORTANT)
client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"]
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

env = RyvoxEmailEnvironment()


def fallback_action(email):
    email = email.lower()
    if "win" in email:
        return "spam"
    elif "meeting" in email:
        return "important"
    else:
        return "normal"


def get_ai_action(email):
    prompt = f"Classify email as spam, important, or normal:\n{email}"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip().lower()

    except Exception as e:
        print(f"[DEBUG] API error: {e}", flush=True)
        return fallback_action(email)


def run():
    rewards = []
    steps = 0

    # ✅ CORRECT START FORMAT
    print(f"[START] task=ryvox env=email model={MODEL_NAME}")

    for i in range(3):  # 🔥 EXACT 3 TASKS
        obs = env.reset()
        email = obs.email_text

        action_value = get_ai_action(email)
        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        steps += 1
        rewards.append(reward)

        # ✅ CORRECT STEP FORMAT
        print(f"[STEP] step={steps} action={action_value} reward={reward:.2f} done=true error=null")

    score = sum(rewards) / len(rewards)
    success = score > 0.1

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    # ✅ CORRECT END FORMAT
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run()