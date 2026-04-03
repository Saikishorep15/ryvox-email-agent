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
    print("🚀 Starting Evaluation...\n")

    total_reward = 0
    episodes = 5

    for i in range(episodes):
        print(f"--- Episode {i+1} ---")

        res = requests.post(f"{BASE_URL}/reset")
        data = res.json()["observation"]

        email = data["email_text"]
        print(f"📩 Email: {email}")

        action = fallback_action(email)
        print(f"🤖 Action: {action}")

        res = requests.post(f"{BASE_URL}/step", json={"action": action})
        result = res.json()

        reward = result["reward"]
        total_reward += reward

        print(f"🎯 Reward: {reward}\n")

    final_score = total_reward / episodes
    print(f"📊 FINAL SCORE: {round(final_score, 2)}")

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