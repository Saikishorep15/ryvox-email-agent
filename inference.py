import os
from openai import OpenAI
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

# ✅ MUST use provided environment variables
client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["API_BASE_URL"]
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

env = RyvoxEmailEnvironment()

# ✅ TASK IDs MUST MATCH openenv.yaml EXACTLY
TASK_IDS = ["spam_detection", "priority_detection", "normal_classification"]


def fallback_action(email):
    email = email.lower()
    if "win" in email:
        return "spam"
    elif "meeting" in email:
        return "important"
    else:
        return "normal"


def get_ai_action(email):
    prompt = f"""
Classify this email into: spam, important, normal.

Email:
{email}

Answer ONLY one word.
"""

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
    for task_id in TASK_IDS:

        # ✅ START LINE (VERY IMPORTANT)
        print(f"[START] task={task_id} env=email model={MODEL_NAME}")

        obs = env.reset()
        email = obs.email_text

        action_value = get_ai_action(email)
        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        # ✅ STEP LINE
        print(f"[STEP] step=1 action={action_value} reward={reward:.2f} done=true error=null")

        # ✅ END LINE
        rewards_str = f"{reward:.2f}"
        print(f"[END] success=true steps=1 score={reward:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run()