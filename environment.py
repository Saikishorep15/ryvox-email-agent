import random
from models import RyvoxEmailObservation, RyvoxEmailAction


class RyvoxEmailEnvironment:
    def __init__(self):
        random.seed(42)

        # 🔥 EXACTLY 3 TASKS
        self.dataset = [
            {"text": "Win $1000 now!", "label": "spam", "task": "spam_detection"},
            {"text": "Project meeting at 5 PM", "label": "important", "task": "priority_detection"},
            {"text": "Hey, how are you?", "label": "normal", "task": "normal_classification"},
        ]

        self.index = 0
        self.current_task = None

    # 🔹 RESET
    def reset(self):
        self.current_task = self.dataset[self.index % len(self.dataset)]
        self.index += 1

        return RyvoxEmailObservation(
            email_text=self.current_task["text"],
            reward=0.1,
            done=False,
            task=self.current_task["task"]   # ✅ ADDED
        )

    # 🔹 STEP
    def step(self, action: RyvoxEmailAction):
        if not self.current_task:
            self.current_task = self.dataset[0]

        try:
            action_value = str(action.action).lower().strip()
        except:
            action_value = ""

        task_type = self.current_task["task"]

        # 🔥 TASK GRADER
        if task_type == "spam_detection":
            reward = 0.85 if action_value == "spam" else 0.15

        elif task_type == "priority_detection":
            reward = 0.85 if action_value == "important" else 0.15

        elif task_type == "normal_classification":
            reward = 0.85 if action_value == "normal" else 0.15

        else:
            reward = 0.2

        # 🔥 STRICT RANGE
        reward = float(reward)
        reward = max(0.1, min(0.9, reward))

        obs = RyvoxEmailObservation(
            email_text="Task Complete",
            reward=reward,
            done=True,
            task=self.current_task["task"]   # ✅ VERY IMPORTANT
        )

        return obs, reward, True, {}

    # 🔹 STATE
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