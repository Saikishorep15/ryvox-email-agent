from environment import RyvoxEmailEnvironment
from models import RyvoxEmailAction

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

    env = RyvoxEmailEnvironment()

    total_reward = 0

    # 🔁 Evaluation Loop (Hackathon requirement ✅)
    for i in range(5):
        print(f"\n--- Episode {i+1} ---")

        obs = env.reset()
        email = obs.email_text

        print(f"📩 Email: {email}")

        action_value = fallback_action(email)
        print(f"🤖 Action: {action_value}")

        action = RyvoxEmailAction(action=action_value)

        obs, reward, done, _ = env.step(action)

        print(f"🎯 Reward: {reward}")

        total_reward += reward

    print("\n📊 FINAL SCORE:", round(total_reward / 5, 2))


if __name__ == "__main__":
    run()