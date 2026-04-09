import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        # 🔥 FIX: Added TASK FIELD (MANDATORY)
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "task": "spam_detection"},
            {"text": "Limited time offer just for you", "label": "spam", "task": "spam_detection"},
            {"text": "URGENT: Update your bank details now", "label": "spam", "task": "spam_detection"},

            {"text": "Project meeting at 5 PM", "label": "important", "task": "priority_detection"},
            {"text": "Client meeting scheduled for tomorrow", "label": "important", "task": "priority_detection"},
            {"text": "Let's discuss the financial report tomorrow", "label": "important", "task": "priority_detection"},

            {"text": "Hey, how are you?", "label": "normal", "task": "normal_classification"},
            {"text": "Lunch at 2?", "label": "normal", "task": "normal_classification"}
        ]

        self.current_task = None
        self.steps = 0
        self.max_steps = 3

    # 🔹 RESET
    def reset(self):
        self.current_task = random.choice(self.dataset)
        self.steps = 0

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.5,   # safe (not 0)
            done=False
        )

    # 🔹 STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = random.choice(self.dataset)

        self.steps += 1

        try:
            action_value = str(action.action).lower().strip()
        except:
            action_value = ""

        correct_label = self.current_task["label"]

        # 🎯 SIMPLIFIED + SAFE REWARD
        if action_value == correct_label:
            reward = 0.8   # correct
        else:
            reward = 0.2   # wrong

        # 🔥 STRICT RANGE (MANDATORY)
        reward = max(0.1, min(0.9, reward))

        done = True   # single-step task (important for grading)

        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=done
        )

        return obs, reward, done, {}

    # 🔹 STATE
    def state(self):
        if not self.current_task:
            return {}

        return {
            "email_text": self.current_task["text"],
            "label": self.current_task["label"],
            "task": self.current_task["task"]
        }

    def close(self):
        pass