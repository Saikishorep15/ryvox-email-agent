import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)
        # Dataset with difficulty levels
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "difficulty": "easy"},
            {"text": "Limited time offer just for you", "label": "spam", "difficulty": "medium"},
            {"text": "Let's discuss the financial report tomorrow", "label": "important", "difficulty": "hard"},
            {"text": "Project meeting at 5 PM", "label": "important", "difficulty": "easy"},
            {"text": "Hey, how are you?", "label": "normal", "difficulty": "easy"}
        ]
        self.current_task = None

    # 🔹 RESET
    def reset(self):
        self.current_task = random.choice(self.dataset)

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.0,
            done=False
        )

    # 🔹 STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = random.choice(self.dataset)

        # Extract action safely
        try:
            if isinstance(action.action, dict):
                action_value = action.action.get("action", "").lower()
            else:
                action_value = str(action.action).lower()
        except Exception:
            action_value = ""

        correct_label = self.current_task["label"]
        email_text = self.current_task["text"].lower()
        difficulty = self.current_task["difficulty"]

        # 🎯 Reward logic (0.0 → 1.0 scale with partial signals)
        if action_value == correct_label:
            if difficulty == "easy":
                reward = 0.3
            elif difficulty == "medium":
                reward = 0.6
            else:
                reward = 1.0

        elif "win" in email_text or "offer" in email_text or "money" in email_text:
            reward = 0.3 if action_value == "spam" else -0.2

        elif "meeting" in email_text or "discuss" in email_text:
            reward = 0.3 if action_value == "important" else -0.2

        else:
            reward = 0.3 if action_value == "normal" else -0.2

        # Observation after step
        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=True
        )

        return obs, reward, True, {}

    # 🔹 STATE (OpenEnv required)
    def state(self):
        if not self.current_task:
            return {}

        return {
            "email_text": self.current_task["text"],
            "label": self.current_task["label"],
            "difficulty": self.current_task["difficulty"]
        }

    # 🔹 CLOSE (optional)
    def close(self):
        pass