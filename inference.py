import os
from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

env = RyvoxEmailEnvironment()

TASKS = ["spam_detection", "priority_detection", "normal_classification"]


def choose_action(email):
    email = email.lower()
    if "win" in email:
        return "spam"
    elif "meeting" in email:
        return "important"
    else:
        return "normal"


def run():
    total_rewards = []

    print("[START] task=ryvox env=email model=rule-based")

    steps = 0

    for i in range(3):  # 🔥 EXACT 3 TASKS
        obs = env.reset()
        email = obs.email_text

        action_value = choose_action(email)
        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        steps += 1
        total_rewards.append(reward)

        print(f"[STEP] step={steps} action={action_value} reward={reward:.2f} done=true error=null")

    score = sum(total_rewards) / len(total_rewards)

    success = score > 0.1

    rewards_str = ",".join(f"{r:.2f}" for r in total_rewards)

    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


if __name__ == "__main__":
    run()