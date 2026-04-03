import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        # Dataset with difficulty levels (3+ tasks)
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "difficulty": "easy"},
            {"text": "Limited time offer just for you", "label": "spam", "difficulty": "medium"},
            {"text": "Let's discuss the financial report tomorrow", "label": "important", "difficulty": "hard"},
            {"text": "Project meeting at 5 PM", "label": "important", "difficulty": "easy"},
            {"text": "Hey, how are you?", "label": "normal", "difficulty": "easy"}
        ]

        self.current_task = None
        self.current_index = 0  # ✅ for reproducibility

    # 🔹 RESET (Deterministic)
    def reset(self):
        self.current_task = self.dataset[self.current_index % len(self.dataset)]
        self.current_index += 1

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.0,
            done=False
        )

    # 🔹 GRADER (Hackathon Requirement ⭐)
    def grade(self, action_value, correct_label, difficulty):
        if action_value == correct_label:
            if difficulty == "easy":
                return 0.3
            elif difficulty == "medium":
                return 0.6
            else:
                return 1.0
        return 0.0

    # 🔹 STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.reset()

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

        # 🎯 Base reward from grader
        reward = self.grade(action_value, correct_label, difficulty)

        # 🎯 Partial reward shaping (learning signal)
        if reward == 0.0:
            if "win" in email_text or "offer" in email_text or "money" in email_text:
                reward = 0.3 if action_value == "spam" else -0.2

            elif "meeting" in email_text or "discuss" in email_text:
                reward = 0.3 if action_value == "important" else -0.2

            else:
                reward = 0.3 if action_value == "normal" else -0.2

        # Observation
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
            "task_id": self.current_index,
            "email_text": self.current_task["text"],
            "label": self.current_task["label"],
            "difficulty": self.current_task["difficulty"]
        }

    # 🔹 CLOSE
    def close(self):
        pass