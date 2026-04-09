import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        # 🔥 PROPER TASK-BASED DATASET
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "task": "spam_detection"},
            {"text": "Limited time offer just for you", "label": "spam", "task": "spam_detection"},

            {"text": "Project meeting at 5 PM", "label": "important", "task": "priority_detection"},
            {"text": "Client meeting tomorrow", "label": "important", "task": "priority_detection"},

            {"text": "Hey, how are you?", "label": "normal", "task": "normal_classification"},
            {"text": "Lunch at 2?", "label": "normal", "task": "normal_classification"},
        ]

        self.current_task = None

    # RESET
    def reset(self):
        self.current_task = random.choice(self.dataset)

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.5,
            done=False
        )

    # STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = random.choice(self.dataset)

        try:
            action_value = str(action.action).lower().strip()
        except:
            action_value = ""

        correct_label = self.current_task["label"]
        task_type = self.current_task["task"]

        # 🔥 TASK-SPECIFIC GRADER
        if task_type == "spam_detection":
            if action_value == "spam":
                reward = 0.85
            else:
                reward = 0.15

        elif task_type == "priority_detection":
            if action_value == "important":
                reward = 0.85
            else:
                reward = 0.15

        elif task_type == "normal_classification":
            if action_value == "normal":
                reward = 0.85
            else:
                reward = 0.15

        else:
            reward = 0.2

        # 🔥 STRICT RANGE FIX
        reward = max(0.1, min(0.9, reward))

        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=True
        )

        return obs, reward, True, {}

    def state(self):
        if not self.current_task:
            return {}

        return {
            "email_text": self.current_task["text"],
            "task": self.current_task["task"],
            "label": self.current_task["label"]
        }

    def close(self):
        pass